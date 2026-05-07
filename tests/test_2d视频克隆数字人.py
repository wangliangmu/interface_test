import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path, poll_until
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.smoke
@pytest.mark.clone
class Test2d视频克隆数字人:
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

    def test_step_02_post_human_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "2D视频{{$date.now|format('MMdd_HHmm')}}",
    "type": 3,
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/cb35e531-63e4-4ff4-bb19-74e5dca0adcc.mp4"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["video_clone_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["video_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{video_clone_id}}"
}
        body = resolve_dict(body, self.context)
        poll_config = {**DEFAULT_POLL_CONFIG, "max_retries": 480}
        response = poll_until(self.session, url, body, headers, poll_config, self.context)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_list(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/list"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "page": 1,
    "page_size": 10,
    "org": 2,
    "type": 3
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_human_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{video_clone_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
