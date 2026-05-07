import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

class Test创建网页类型对话带动作:
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
    "name": "网页_接口测试_带动作{{$date.now|format('MMdd_HHmm')}}",
    "type": "2d",
    "machine_type": 1,
    "scale": "16:9"
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
    "id": "{{dialogs_id}}",
    "name": "网页_接口测试_带动作{{$date.now|format('MMdd_HHmm')}}",
    "type": "2d",
    "machine_type": 1,
    "agent_type": 1,
    "bot_id": "",
    "create_time": 1778128238,
    "update_time": 1778128381,
    "scale": "16:9",
    "human_id": 2654,
    "voice_id": 0,
    "expand": "{\"bg\":{\"size\":{\"width\":1920,\"height\":1080}},\"human\":{\"position\":{\"x\":660,\"y\":7},\"scale\":{\"x\":1,\"y\":1},\"size\":{\"width\":600,\"height\":1067},\"source\":{\"id\":2654,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\"}},\"page\":[{\"id\":\"[drag]-human\",\"source\":{\"id\":2654,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\"},\"style\":{\"height\":1067,\"scaleX\":1,\"scaleY\":1,\"width\":600,\"x\":660,\"y\":7,\"zIndex\":1},\"type\":\"Human\",\"visible\":true}],\"voice\":{},\"actionMap\":{\"broadCast\":[449,448,447,446]},\"interrupted_video\":[\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123306_216eadd8f9.flv\",\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123433_ae2558738f.flv\",\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123515_885e4ac9d0.flv\"],\"output_size\":{\"width\":1920,\"height\":1080}}",
    "word_action": "",
    "word_ssml": "",
    "word": "",
    "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/e3cfc2fe-a01b-49a7-9a80-4060184c3e04.jpeg",
    "speak_rate": 0,
    "qa_id": 0,
    "bg_path": "",
    "bc_path": "",
    "status": "success",
    "reason": "",
    "is_default": 2,
    "style": 0,
    "knowledge_ids": None,
    "nickname": "",
    "temperature": 0,
    "mark": False,
    "backupChat": False,
    "tipsText": "",
    "chatMode": 1,
    "isMulChat": 0,
    "actionType": 0,
    "prompt": "",
    "difyBotId": "",
    "interaction": "{\"greet\":{\"hostess_mode\":true,\"welcome_wordlist\":[\"您好[称呼]，有什么可以帮您？\"],\"face_sourceid\":\"\"},\"revoke\":{\"wake_words\":\"你好小初\",\"covert_wake_words\":\"n ǐ h ǎo x iǎo ch ū @你好小初\"},\"hotword\":{\"hotword_sourceid\":\"\"}}",
    "appConfig": "{}"
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
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

