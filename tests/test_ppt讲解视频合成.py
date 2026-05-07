import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.ai
class TestPpt讲解视频合成:
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

    def test_step_02_post_14_compose(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/drafts/14/compose"
        url = resolve_template(url, self.context)
        headers = {}
        body = {
    "id": 14,
    "name": "PPT视频{{$date.now|format('MMdd_HHmm')}}",
    "quality": "1080P",
    "format": "MP4"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
        )
        try:
            self.context["compose_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["compose_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_get_pptvideo_taskspage_size1page1typeppttask_typev(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/tasks?page_size=1&page=1&type=ppt&task_type=video_merge"
        url = resolve_template(url, self.context)
        headers = {
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        response = self.session.request(
            method="GET",
            url=url,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_delete_pptvideo_tasks(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/tasks/{{compose_id}}"
        url = resolve_template(url, self.context)
        headers = {}
        response = self.session.request(
            method="DELETE",
            url=url,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

