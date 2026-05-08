import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.clone
class Test志强基础版声音克隆:
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

    def test_step_02_post_voiceclone_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "测试1",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/9756fa15-aca9-4dc6-b99a-3db855f3ceec.wav"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["voice_clone_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["voice_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_voiceclone_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": "{{voice_clone_id}}"
}
        body = resolve_dict(body, self.context)
        
        max_retries = 30
        wait_interval = 20
        response = None
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method="POST",
                    url=url,
                    json=body,
                    headers=headers,
                )
                assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
                
                response_json = response.json()
                status = extract_json_path(response_json, "$.data.data.status")
                
                if status in ["normal", "failed"]:
                    break
                elif status == "producing":
                    print(f"Status is 'producing', waiting {wait_interval} seconds...")
                    time.sleep(wait_interval)
                else:
                    print(f"Unknown status: {status}, continuing to poll...")
                    time.sleep(wait_interval)
            except Exception as e:
                print(f"Error occurred, skipping to next iteration: {e}")
                time.sleep(wait_interval)
        
        assert response is not None, "No response received after polling"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        
        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.data.status")
            assert status == "normal", f"Expected status 'normal', got '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"Failed to parse response or check status: {e}"

