import re
import json
import jsonpath_ng
from datetime import datetime, timezone, timedelta


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
            if isinstance(value, (int, float, bool)) and not isinstance(value, bool):
                return str(value)
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
            print(f"Poll attempt {attempt+1}/{max_retries}: HTTP {response.status_code}")
            sleep(wait_interval)
            continue
        
        try:
            data = response.json()
            current_status = extract_json_path(data, poll_expression)
            
            if current_status in expected_statuses:
                print(f"Poll attempt {attempt+1}/{max_retries}: Task completed successfully (status={current_status!r})")
                return response
            
            if current_status in error_statuses:
                raise RuntimeError(f"Task failed with status: {current_status}")
            
            print(f"Poll attempt {attempt+1}/{max_retries}: Current status = {current_status!r}, waiting...")
        
        except json.JSONDecodeError:
            print(f"Poll attempt {attempt+1}/{max_retries}: Failed to parse JSON response")
        except Exception as e:
            print(f"Poll attempt {attempt+1}/{max_retries}: Error - {str(e)}")
        
        sleep(wait_interval)
    
    raise TimeoutError(f"Polling timeout after {max_retries * wait_interval} seconds")
