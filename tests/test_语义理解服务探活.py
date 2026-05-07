import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.ai
class Test语义理解服务探活:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_post_infer_11120(self):
        self._apply_common_headers()
        url = "https://platform-h20.wair.ac.cn/api/v1/infer/11120"
        headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiJ9.j6-hUMaFYdSIzfc6i6TJ5DaS96Z9I78SrjxAOg-71yE"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "query": "切换数字人",
    "base_id": 10000
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

