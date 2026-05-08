import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.dialog
class Test创建手机类型对话:
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

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "手机_接口测试{{$date.now|format('MMdd_HHmm')}}",
    "type": "2d",
    "machine_type": 3,
    "scale": "9:16"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["dialogs_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "_raw": "{\r\n    \"id\": {{dialogs_id}},\r\n    \"name\": \"手机_接口测试DATE_FORMAT_PLACEHOLDER\",\r\n    \"type\": \"2d\",\r\n    \"machine_type\": 3,\r\n    \"agent_type\": 1,\r\n    \"bot_id\": \"\",\r\n    \"create_time\": 1778202052,\r\n    \"update_time\": 1778202052,\r\n    \"scale\": \"9:16\",\r\n    \"human_id\": 4438,\r\n    \"voice_id\": 0,\r\n    \"background_id\": 7951,\r\n    \"expand\": \"{\\\"bg\\\":{\\\"source\\\":{\\\"id\\\":7951,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/7b54c3a1-223d-499b-9240-c6ea8f4d1bbf.png\\\"},\\\"size\\\":{\\\"width\\\":1080,\\\"height\\\":1920}},\\\"human\\\":{\\\"position\\\":{\\\"x\\\":100,\\\"y\\\":178},\\\"scale\\\":{\\\"x\\\":1,\\\"y\\\":1},\\\"size\\\":{\\\"width\\\":880,\\\"height\\\":1564},\\\"source\\\":{\\\"id\\\":4438,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/紫瑶.png\\\"}},\\\"page\\\":[{\\\"id\\\":\\\"[drag]-human\\\",\\\"type\\\":\\\"Human\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"x\\\":100,\\\"y\\\":178,\\\"scaleX\\\":1,\\\"scaleY\\\":1,\\\"width\\\":880,\\\"height\\\":1564,\\\"zIndex\\\":1},\\\"source\\\":{\\\"id\\\":4438,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/紫瑶.png\\\"}}],\\\"voice\\\":{},\\\"actionMap\\\":{},\\\"output_size\\\":{\\\"width\\\":1080,\\\"height\\\":1920}}\",\r\n    \"word_action\": \"\",\r\n    \"word_ssml\": \"\",\r\n    \"word\": \"\",\r\n    \"cover_img\": \"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/af34fb24-3eb1-4e2b-84af-889e57750697.jpeg\",\r\n    \"speak_rate\": 0,\r\n    \"qa_id\": 0,\r\n    \"bg_path\": \"\",\r\n    \"bc_path\": \"\",\r\n    \"status\": \"normal\",\r\n    \"reason\": \"\",\r\n    \"is_default\": 2,\r\n    \"style\": 0,\r\n    \"knowledge_ids\": None,\r\n    \"nickname\": \"\",\r\n    \"temperature\": 0,\r\n    \"mark\": False,\r\n    \"backupChat\": False,\r\n    \"tipsText\": \"\",\r\n    \"chatMode\": 0,\r\n    \"isMulChat\": 0,\r\n    \"actionType\": 0,\r\n    \"prompt\": \"\",\r\n    \"difyBotId\": \"\",\r\n    \"interaction\": \"{\\\"greet\\\":{\\\"hostess_mode\\\":True,\\\"welcome_wordlist\\\":[\\\"您好[称呼]，有什么可以帮您？\\\"],\\\"face_sourceid\\\":\\\"\\\"},\\\"revoke\\\":{\\\"wake_words\\\":\\\"你好小初\\\",\\\"covert_wake_words\\\":\\\"n ǐ h ǎo x iǎo ch ū @你好小初\\\"},\\\"hotword\\\":{\\\"hotword_sourceid\\\":\\\"\\\"}}\",\r\n    \"appConfig\": \"{}\"\r\n}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_dialogs_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": "{{dialogs_id}}"
}
        body = resolve_dict(body, self.context)
        
        max_retries = 18
        wait_interval = 30
        response = None
        
        for attempt in range(max_retries):
            response = self.session.request(
                method="POST",
                url=url,
                json=body,
                headers=headers,
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
            
            try:
                response_json = response.json()
                status = extract_json_path(response_json, "$.data.data.status")
                
                if status in ["success", "failed"]:
                    break
                elif status == "producing":
                    print(f"Status is 'producing', waiting {wait_interval} seconds...")
                    time.sleep(wait_interval)
                else:
                    print(f"Unknown status: {status}, continuing to poll...")
                    time.sleep(wait_interval)
            except Exception as e:
                print(f"Failed to parse status: {e}")
                time.sleep(wait_interval)
        
        assert response is not None, "No response received after polling"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        
        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.data.status")
            assert status == "success", f"Expected status 'success', got '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"Failed to parse response or check status: {e}"

