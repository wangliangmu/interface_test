import re
import json
import time
import logging
import jsonpath_ng
import requests
from datetime import datetime, timezone, timedelta
from functools import wraps

logger = logging.getLogger("api_test")

MAX_RESPONSE_LOG_LENGTH = 5000
SENSITIVE_HEADER_KEYS = {"authorization", "token", "cookie", "set-cookie"}

RETRY_STATUS_CODES = {500, 502, 503, 504}
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_DELAY = 5


class LoggingSession(requests.Session):
    def request(self, method, url, **kwargs):
        logger.info("=" * 80)
        logger.info("REQUEST >>> %s %s", method, url)

        req_headers = kwargs.get("headers") or {}
        if req_headers:
            safe_headers = _mask_sensitive_headers(dict(req_headers))
            logger.info("Request Headers:\n%s", json.dumps(safe_headers, ensure_ascii=False, indent=2))

        req_json = kwargs.get("json")
        req_data = kwargs.get("data")
        if req_json is not None:
            body_str = json.dumps(req_json, ensure_ascii=False, indent=2) if isinstance(req_json, (dict, list)) else str(req_json)
            logger.info("Request Body:\n%s", body_str)
        elif req_data is not None:
            logger.info("Request Data:\n%s", str(req_data)[:MAX_RESPONSE_LOG_LENGTH])

        start_time = time.time()
        response = super().request(method, url, **kwargs)
        elapsed_ms = (time.time() - start_time) * 1000

        logger.info("RESPONSE <<< %s (耗时: %.0fms)", response.status_code, elapsed_ms)

        resp_headers = dict(response.headers)
        safe_resp_headers = _mask_sensitive_headers(resp_headers)
        logger.info("Response Headers:\n%s", json.dumps(safe_resp_headers, ensure_ascii=False, indent=2))

        try:
            resp_json = response.json()
            resp_str = json.dumps(resp_json, ensure_ascii=False, indent=2)
            if len(resp_str) > MAX_RESPONSE_LOG_LENGTH:
                resp_str = resp_str[:MAX_RESPONSE_LOG_LENGTH] + "\n... (截断，总长度: %d 字符)" % len(resp_str)
            logger.info("Response Body:\n%s", resp_str)
        except (json.JSONDecodeError, ValueError):
            text = response.text[:MAX_RESPONSE_LOG_LENGTH]
            logger.info("Response Body (text):\n%s", text)

        logger.info("=" * 80)

        return response


def _mask_sensitive_headers(headers):
    masked = {}
    for k, v in headers.items():
        if k.lower() in SENSITIVE_HEADER_KEYS:
            val_str = str(v)
            masked[k] = "****" + val_str[-4:] if len(val_str) > 4 else "****"
        else:
            masked[k] = v
    return masked


def resolve_template(text: str, context: dict) -> str:
    if not isinstance(text, str):
        return text
    
    def replacer(match):
        var_name = match.group(1)
        if var_name.startswith("$date"):
            beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
            return beijing_time.strftime("%m%d_%H%M")
        if var_name in context:
            value = context[var_name]
            if value is None:
                return ''
            return str(value)
        return match.group(0)
    
    return re.sub(r'\{\{(\S+?)\}\}', replacer, text)


def resolve_dict(d, context: dict):
    if isinstance(d, dict):
        result = {}
        raw_value = None
        for k, v in d.items():
            if k == '_raw' and isinstance(v, str):
                processed = resolve_template(v, context)
                processed = re.sub(r'\bTrue\b', 'true', processed)
                processed = re.sub(r'\bFalse\b', 'false', processed)
                processed = re.sub(r'\bNone\b', 'null', processed)
                try:
                    raw_value = json.loads(processed)
                except (json.JSONDecodeError, ValueError):
                    raw_value = processed
                continue
            if isinstance(v, str):
                processed = resolve_template(v, context)
                if v.startswith('{{') and v.endswith('}}'):
                    try:
                        if processed.lower() == 'true':
                            result[k] = True
                        elif processed.lower() == 'false':
                            result[k] = False
                        elif processed.lower() == 'null':
                            result[k] = None
                        else:
                            if '.' in processed:
                                result[k] = float(processed)
                            else:
                                result[k] = int(processed)
                    except (ValueError, TypeError):
                        result[k] = processed
                else:
                    result[k] = processed
            else:
                result[k] = resolve_dict(v, context)
        if raw_value is not None:
            if isinstance(raw_value, dict):
                raw_value.update(result)
                result = raw_value
            else:
                result['_raw'] = raw_value
        return result
    elif isinstance(d, list):
        return [resolve_dict(v, context) for v in d]
    elif isinstance(d, str):
        return resolve_template(d, context)
    return d


def extract_json_path(data, path: str):
    expr = jsonpath_ng.parse(path)
    matches = expr.find(data)
    if matches:
        return matches[0].value
    return None


def retry_on_server_errors(max_retries=DEFAULT_RETRY_COUNT, delay=DEFAULT_RETRY_DELAY):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    if response.status_code in RETRY_STATUS_CODES:
                        logger.warning(f"请求失败，HTTP状态码 {response.status_code}，第 {attempt + 1}/{max_retries} 次尝试")
                        last_exception = Exception(f"HTTP {response.status_code}: {response.text[:200]}")
                        time.sleep(delay * (2 ** attempt))
                        continue
                    return response
                except requests.exceptions.RequestException as e:
                    logger.warning(f"请求异常: {e}，第 {attempt + 1}/{max_retries} 次尝试")
                    last_exception = e
                    time.sleep(delay * (2 ** attempt))

            logger.error(f"请求失败，已重试 {max_retries} 次")
            if last_exception:
                raise last_exception
            raise Exception(f"请求失败，已重试 {max_retries} 次")
        return wrapper
    return decorator


class RetrySession(requests.Session):
    def __init__(self, max_retries=DEFAULT_RETRY_COUNT, delay=DEFAULT_RETRY_DELAY):
        super().__init__()
        self.max_retries = max_retries
        self.delay = delay

    def request(self, method, url, **kwargs):
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = super().request(method, url, **kwargs)
                if response.status_code in RETRY_STATUS_CODES:
                    logger.warning(f"请求失败，HTTP状态码 {response.status_code}，第 {attempt + 1}/{self.max_retries} 次尝试")
                    last_exception = Exception(f"HTTP {response.status_code}: {response.text[:200]}")
                    time.sleep(self.delay * (2 ** attempt))
                    continue
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求异常: {e}，第 {attempt + 1}/{self.max_retries} 次尝试")
                last_exception = e
                time.sleep(self.delay * (2 ** attempt))

        logger.error(f"请求失败，已重试 {self.max_retries} 次")
        if last_exception:
            raise last_exception
        raise Exception(f"请求失败，已重试 {self.max_retries} 次")


def poll_until(session, url, body, headers, poll_config, context=None):
    max_retries = poll_config.get("max_retries", 30)
    wait_interval = poll_config.get("wait_interval", 5)
    poll_expression = poll_config.get("poll_expression", "$.data.status")
    expected_statuses = poll_config.get("poll_expected_list", ["completed", "normal", "success"])
    error_statuses = poll_config.get("error_statuses", ["failed", "error", "rejected", "timeout", "canceled"])

    from time import sleep

    for attempt in range(max_retries):
        response = session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers
        )

        if response.status_code != 200:
            logger.warning("Poll attempt %d/%d: HTTP %s", attempt + 1, max_retries, response.status_code)
            sleep(wait_interval)
            continue

        try:
            data = response.json()
            current_status = extract_json_path(data, poll_expression)

            if current_status in expected_statuses:
                logger.info("Poll attempt %d/%d: Task completed successfully (status=%r)", attempt + 1, max_retries, current_status)
                return response

            if current_status in error_statuses:
                raise RuntimeError(f"Task failed with status: {current_status}")

            logger.info("Poll attempt %d/%d: Current status = %r, waiting...", attempt + 1, max_retries, current_status)

        except json.JSONDecodeError:
            logger.warning("Poll attempt %d/%d: Failed to parse JSON response", attempt + 1, max_retries)
        except Exception as e:
            logger.error("Poll attempt %d/%d: Error - %s", attempt + 1, max_retries, str(e))

        sleep(wait_interval)

    raise TimeoutError(f"Polling timeout after {max_retries * wait_interval} seconds")
