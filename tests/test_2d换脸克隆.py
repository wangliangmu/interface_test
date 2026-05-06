import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.clone
class Test2d换脸克隆:
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

    def test_step_02_post_human_faceSwap(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/faceSwap"
        url = resolve_template(url, self.context)
        headers = {}
        body = {
    "name": "自动化接口测试",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/178/00abf0c3-c0ff-497f-ad4a-7da13799c927.jpg",
    "id": 3162
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
        )
        try:
            self.context["faceswap_task_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["faceswap_task_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {}
        body = {
    "human_id": "{{faceswap_task_id}}"
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

    def test_step_05_post_human_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/delete"
        url = resolve_template(url, self.context)
        headers = {
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{faceswap_task_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

