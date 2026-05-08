import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG


@pytest.mark.ai
class TestAi卡通照片接口测试:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_post_account_login(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/account/login"
        url = resolve_template(url, self.context)
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        headers = resolve_dict(headers, self.context)
        body = {
            "source": "show",
            "username": "auto_test_jxm",
            "password": "auto_test_jxm123",
            "permission": "on",
        }
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["token"] = extract_json_path(response.json(), "$.data.token")
        except Exception:
            self.context["token"] = None
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_02_post_img2img_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/ai/img2img/add"
        url = resolve_template(url, self.context)
        headers = {
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
        }
        headers = resolve_dict(headers, self.context)
        body = {
            "prompt": "日漫",
            "resolution": "1382x1382",
            "url": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/178/516651ce-52c1-441d-93c4-1e95d5684a3a.png",
            "server_type": "img2cartoon",
        }
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["img2img_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["img2img_id"] = None
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_ai_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/ai/get"
        url = resolve_template(url, self.context)
        headers = {
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
        }
        headers = resolve_dict(headers, self.context)
        body = {"id": "{{img2img_id}}"}
        body = resolve_dict(body, self.context)

        wait_seconds = 60
        print(f"Waiting {wait_seconds} seconds for AI cartoon photo generation...")
        time.sleep(wait_seconds)

        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"
