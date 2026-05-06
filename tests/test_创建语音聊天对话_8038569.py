import pytest
import requests
import json
import re
import time
from datetime import datetime

BASE_URL = "https://metahuman-prod.wair.ac.cn"
COMMON_HEADERS = [
    {
        "name": "token",
        "value": "{{token}}",
        "enable": True
    },
    {
        "name": "Authorization",
        "value": "Bearer {{token}}",
        "enable": True
    },
    {
        "name": "auto-gen-qa-tasks_id",
        "value": "{{auto-gen-qa-tasks_id}}",
        "enable": True
    }
]


def resolve_template(text, context):
    if not isinstance(text, str):
        return text
    def replacer(match):
        var_name = match.group(1)
        if var_name.startswith("$date"):
            return datetime.now().strftime("%m%d_%H%M")
        if var_name in context:
            return str(context[var_name])
        return match.group(0)
    return re.sub(r'\{\{(\S+?)\}\}', replacer, text)


def resolve_dict(d, context):
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            if isinstance(v, str):
                import re
                match = re.search(r'\{\{(\w+)\}\}', v)
                if match:
                    var_name = match.group(1)
                    result[k] = context.get(var_name, v)
                else:
                    result[k] = resolve_template(v, context)
            else:
                result[k] = resolve_dict(v, context)
        return result
    elif isinstance(d, list):
        return [resolve_dict(v, context) for v in d]
    elif isinstance(d, str):
        return resolve_template(d, context)
    return d


def extract_json_path(data, path):
    import jsonpath_ng
    expr = jsonpath_ng.parse(path)
    matches = expr.find(data)
    if matches:
        return matches[0].value
    return None


class Test创建语音聊天对话:
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
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "语音聊天_自动化接口测试",
    "machine_type": 4,
    "type": "",
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

    def test_step_04_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": "{{dialogs_id}}",
    "name": "语音聊天_自动化接口测试",
    "type": "2d",
    "machine_type": 4,
    "agent_type": 1,
    "bot_id": "",
    "create_time": 1766541501,
    "update_time": 1766541501,
    "scale": "9:16",
    "human_id": 0,
    "voice_id": 1356,
    "background_id": 0,
    "expand": "",
    "word_action": "",
    "word_ssml": "",
    "word": "",
    "cover_img": "",
    "speak_rate": 0,
    "qa_id": 0,
    "bg_path": "",
    "bc_path": "",
    "status": "normal",
    "reason": "",
    "is_default": 2,
    "style": 0,
    "knowledge_ids": None,
    "nickname": "",
    "temperature": 0,
    "mark": False,
    "backupChat": False,
    "tipsText": "",
    "chatMode": 0,
    "isMulChat": 0,
    "interaction": "{\"greet\":{\"hostess_mode\":True,\"welcome_wordlist\":[\"您好[称呼]，有什么可以帮您？\"],\"face_sourceid\":\"\"},\"revoke\":{\"wake_words\":\"你好小初\",\"covert_wake_words\":\"n ǐ h ǎo x iǎo ch ū @你好小初\"}}",
    "actionType": 0,
    "prompt": "",
    "appConfig": "{\"profile\":{\"avatar\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/48ddcaae-f90e-49cd-bcb8-ea6fbb85dc0b.png\",\"description\":\"你好，这是在做自动化接口测试\"},\"mode\":{\"guideMode\":True,\"spotDistance\":50}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_channel_create(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/channel/create"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "dialogId": "{{dialogs_id}}",
    "channelUserAccount": "jiaxiaomei"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_06_post_dialogs_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": [
        "{{dialogs_id}}"
    ]
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

