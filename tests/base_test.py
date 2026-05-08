import logging

import pytest
import requests

from config import BASE_URL, COMMON_HEADERS
from utils import resolve_template, resolve_dict, extract_json_path


logger = logging.getLogger("api_test")


class BaseTest:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.session.headers.update({"content-type": "application/json"})
        cls.context = {}

    @classmethod
    def teardown_class(cls):
        if cls.session:
            cls.session.close()

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def _request(self, method, url, **kwargs):
        url = resolve_template(url, self.context)

        if "headers" in kwargs:
            kwargs["headers"] = resolve_dict(kwargs["headers"], self.context)

        if "json" in kwargs:
            kwargs["json"] = resolve_dict(kwargs["json"], self.context)

        response = self.session.request(method, url, **kwargs)
        return response

    def _login(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/account/login"
        body = {
            "source": "show",
            "username": "auto_test_jxm",
            "password": "auto_test_jxm123",
            "permission": "on",
        }
        response = self._request("POST", url, json=body, headers={"priority": "u=1, i"})
        assert response.status_code == 200, f"登录失败: {response.text[:200]}"
        try:
            self.context["token"] = extract_json_path(response.json(), "$.data.token")
            logger.info("登录成功，获取到 token")
        except Exception as e:
            logger.error(f"提取 token 失败: {e}")
            self.context["token"] = None
            raise

    def _poll_for_status(
        self,
        url,
        body,
        headers=None,
        max_retries=15,
        wait_interval=30,
        status_path="$.data.status",
        success_statuses=None,
        error_statuses=None,
    ):
        if success_statuses is None:
            success_statuses = ["normal", "success", "completed"]
        if error_statuses is None:
            error_statuses = ["failed", "error", "rejected", "timeout", "canceled"]

        response = None
        for attempt in range(max_retries):
            response = self._request("POST", url, json=body, headers=headers)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

            try:
                response_json = response.json()
                status = extract_json_path(response_json, status_path)

                if status in success_statuses:
                    logger.info(f"轮询成功: 第 {attempt + 1}/{max_retries} 次，状态={status}")
                    return response
                if status in error_statuses:
                    raise RuntimeError(f"任务失败，状态={status}")

                logger.info(f"轮询中: 第 {attempt + 1}/{max_retries} 次，当前状态={status}，等待 {wait_interval} 秒...")
                import time

                time.sleep(wait_interval)
            except json.JSONDecodeError as e:
                logger.warning(f"轮询解析 JSON 失败: {e}")
                import time

                time.sleep(wait_interval)
            except Exception as e:
                logger.error(f"轮询异常: {e}")
                import time

                time.sleep(wait_interval)

        raise TimeoutError(f"轮询超时，已重试 {max_retries} 次，总等待时间 {max_retries * wait_interval} 秒")

    def _assert_status(self, response, expected_status, status_path="$.data.status"):
        try:
            response_json = response.json()
            status = extract_json_path(response_json, status_path)
            assert status == expected_status, f"期望状态 '{expected_status}'，实际状态 '{status}': {response.text[:200]}"
            return status
        except Exception as e:
            pytest.fail(f"解析响应或检查状态失败: {e}")