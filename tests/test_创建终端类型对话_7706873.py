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


class Test创建终端类型对话:
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
    "name": "终端_接口测试",
    "type": "2d",
    "machine_type": 2,
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
    "id": "{{dialogs_id}}",
    "name": "终端_接口测试",
    "type": "2d",
    "machine_type": 2,
    "agent_type": 1,
    "bot_id": "",
    "create_time": 1764829391,
    "update_time": 1764829391,
    "scale": "9:16",
    "human_id": 3726,
    "background_id": 7850,
    "expand": "{\"bg\":{\"size\":{\"width\":1080,\"height\":1920},\"source\":{\"id\":7850,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/46f18c65-9135-437f-ba0a-779d4a5365e0.png\"}},\"human\":{\"position\":{\"x\":-10,\"y\":30},\"scale\":{\"x\":1,\"y\":1},\"size\":{\"width\":1081,\"height\":1922},\"source\":{\"id\":3726,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/小初.png\"}},\"page\":[{\"id\":\"[drag]-dialogue\",\"type\":\"Dialogue\",\"style\":{\"width\":984,\"height\":384,\"x\":48,\"y\":790,\"zIndex\":2,\"scaleX\":1,\"scaleY\":1,\"rotate\":0,\"_userBg\":\"#006AFF\",\"_userColor\":\"#fff\",\"_robotBg\":\"#FFFFFF\",\"_robotColor\":\"#222222\",\"_Type\":\"vertical\"}},{\"id\":\"[drag]-hotRequest\",\"type\":\"HotRequest\",\"style\":{\"width\":764,\"height\":80,\"x\":48,\"y\":124,\"zIndex\":2,\"backgroundColor\":\"rgba(26, 26, 26, 0.5)\",\"color\":\"#FFFFFF\",\"_Type\":\"horizontal\"}},{\"id\":\"[drag]-wifiStatus\",\"type\":\"WifiStatus\",\"visible\":True,\"style\":{\"width\":36,\"height\":36,\"x\":832,\"y\":48,\"zIndex\":2,\"color\":\"#FFFFFF\"}},{\"id\":\"[drag]-timeStatus\",\"type\":\"TimeStatus\",\"visible\":True,\"style\":{\"width\":180,\"height\":36,\"x\":876,\"y\":48,\"zIndex\":2,\"color\":\"#FFFFFF\"}},{\"id\":\"[drag]-camera\",\"type\":\"Camera\",\"style\":{\"width\":210,\"height\":274,\"x\":822,\"y\":124,\"zIndex\":2,\"_tipColor\":\"#000000\",\"_tipBgColor\":\"#FFFFFF\"}},{\"id\":\"[drag]-humanStatus\",\"type\":\"HumanStatus\",\"visible\":True,\"style\":{\"width\":272,\"height\":84,\"x\":404,\"y\":20,\"zIndex\":2,\"color\":\"#FFFFFF\",\"backgroundColor\":\"rgba(51, 51, 51, 0.7)\"},\"source\":{\"path\":\"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_listen.png\"}},{\"id\":\"[drag]-image-logo\",\"type\":\"Image\",\"renderType\":\"image\",\"style\":{\"width\":176,\"height\":40,\"x\":48,\"y\":48,\"zIndex\":101},\"source\":{\"path\":\"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_logo_dark2.png\"}},{\"id\":\"[drag]-changeBtn\",\"type\":\"ChangeBtn\",\"style\":{\"width\":100,\"height\":96,\"x\":932,\"y\":410,\"zIndex\":2,\"backgroundColor\":\"rgba(26, 26, 26, 0.5)\",\"color\":\"#FFFFFF\",\"_iconColor\":\"#FFFFFF\"}},{\"id\":\"[drag]-quitBtn\",\"type\":\"QuitBtn\",\"style\":{\"width\":100,\"height\":96,\"x\":820,\"y\":410,\"zIndex\":2,\"backgroundColor\":\"rgba(26, 26, 26, 0.5)\",\"color\":\"#FFFFFF\",\"_iconColor\":\"#FFFFFF\"}},{\"id\":\"[drag]-human\",\"type\":\"Human\",\"style\":{\"x\":-10,\"y\":30,\"scaleX\":1,\"scaleY\":1,\"width\":1081,\"height\":1922,\"zIndex\":1},\"source\":{\"id\":3726,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/小初.png\"}}],\"voice\":{},\"actionMap\":{}}",
    "word_action": "",
    "word_ssml": "",
    "word": "",
    "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/45804bb0-5ab0-406a-9ae9-23b1dd824bfe.jpeg",
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
    "actionType": 0,
    "prompt": "",
    "interaction": "{\"greet\":{\"hostess_mode\":True,\"welcome_wordlist\":[\"您好[称呼]，有什么可以帮您？\"],\"face_sourceid\":\"\"},\"revoke\":{\"wake_words\":\"你好小初\",\"covert_wake_words\":\"n ǐ h ǎo x iǎo ch ū @你好小初\"}}"
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

    def test_step_06_post_dialogs_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}https://metahuman-prod.wair.ac.cn/metaman/api/dialogs/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
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

