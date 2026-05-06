import pytest
import requests
import json
import time

from .utils import resolve_template, resolve_dict, extract_json_path
from .config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG


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
        
        max_retries = DEFAULT_POLL_CONFIG["max_retries"]
        wait_interval = DEFAULT_POLL_CONFIG["wait_interval"]
        poll_expression = DEFAULT_POLL_CONFIG["poll_expression"]
        poll_expected_list = DEFAULT_POLL_CONFIG["poll_expected_list"]
        error_statuses = DEFAULT_POLL_CONFIG["error_statuses"]
        
        for attempt in range(max_retries):
            response = self.session.request(
                method="POST",
                url=url,
                json=body,
                headers=headers,
            )
            
            if response.status_code != 200:
                print(f"Poll attempt {attempt+1}/{max_retries}: HTTP {response.status_code}")
                time.sleep(wait_interval)
                continue
            
            try:
                data = response.json()
                actual_value = extract_json_path(data, poll_expression)
                
                if actual_value in poll_expected_list:
                    print(f"Poll attempt {attempt+1}/{max_retries}: Task completed successfully (status={actual_value!r})")
                    break
                    
                if actual_value in error_statuses:
                    raise RuntimeError(f"Task failed with status: {actual_value}")
                    
                print(f"Poll attempt {attempt+1}/{max_retries}: Current status = {actual_value!r}, waiting...")
                
            except json.JSONDecodeError:
                print(f"Poll attempt {attempt+1}/{max_retries}: Failed to parse JSON response")
            except Exception as e:
                print(f"Poll attempt {attempt+1}/{max_retries}: Error - {str(e)}")
            
            time.sleep(wait_interval)
        else:
            raise TimeoutError(f"Polling timeout after {max_retries * wait_interval} seconds")
        
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
