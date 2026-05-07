import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path, poll_until
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.clone
class Test3d形象生成:
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

    def test_step_02_post_human_photo_3d_gen(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/photo_3d_gen"
        url = resolve_template(url, self.context)
        headers = {}
        body = {
    "name": "3D形象{{$date.now|format('MMdd_HHmm')}}",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/1a30a0d5-8ded-4bd7-8209-9f9b3bccb8ea.png",
    "sex": "女",
    "server_type": "img2img"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
        )
        try:
            self.context["3d_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["3d_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{3d_id}}"
}
        body = resolve_dict(body, self.context)
        poll_config = {**DEFAULT_POLL_CONFIG, "max_retries": 132}
        response = poll_until(self.session, url, body, headers, poll_config, self.context)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_human_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{3d_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

