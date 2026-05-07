import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.risk
class Test风控测试:
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
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "source": "show",
    "username": "auto_test_jxm",
    "password": "auto_test_jxm123",
    "permission": "on"
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
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_02_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/2055f570-ddfa-414f-a58b-ebec7d32797c.png",
    "type": "image"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/0fef2de4-4328-4773-b267-e013d970b74c.mp4",
    "type": "video"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

