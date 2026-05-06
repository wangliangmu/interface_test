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
    "_raw": "{\r\n    \"id\": {{dialogs_id}},\r\n    \"name\": \"手机_接口测试DATE_FORMAT_PLACEHOLDER\",\r\n    \"type\": \"2d\",\r\n    \"machine_type\": 3,\r\n    \"agent_type\": 1,\r\n    \"bot_id\": \"\",\r\n    \"create_time\": 1761114202,\r\n    \"update_time\": 1761114202,\r\n    \"scale\": \"9:16\",\r\n    \"human_id\": 2654,\r\n    \"voice_id\": 1440,\r\n    \"expand\": \"{\\\"bg\\\":{\\\"size\\\":{\\\"width\\\":1080,\\\"height\\\":1920}},\\\"human\\\":{\\\"position\\\":{\\\"x\\\":-34,\\\"y\\\":-1},\\\"scale\\\":{\\\"x\\\":1,\\\"y\\\":1},\\\"size\\\":{\\\"width\\\":1202,\\\"height\\\":2137},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}},\\\"page\\\":[{\\\"id\\\":\\\"[drag]-human\\\",\\\"type\\\":\\\"Human\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"x\\\":-34,\\\"y\\\":-1,\\\"scaleX\\\":1,\\\"scaleY\\\":1,\\\"width\\\":1202,\\\"height\\\":2137,\\\"zIndex\\\":1},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}}],\\\"voice\\\":{\\\"source\\\":{\\\"id\\\":1440,\\\"name\\\":\\\"S_JM0DTk1B1\\\"}},\\\"actionMap\\\":{}}\",\r\n    \"word_action\": \"\",\r\n    \"word_ssml\": \"\",\r\n    \"word\": \"你好，我是黛玉\",\r\n    \"cover_img\": \"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/64fb7297-5ea3-4790-9074-9f21ea26b007.jpeg\",\r\n    \"speak_rate\": 0,\r\n    \"bg_path\": \"\",\r\n    \"bc_path\": \"\",\r\n    \"status\": \"normal\",\r\n    \"reason\": \"\",\r\n    \"is_default\": 1,\r\n    \"style\": 0,\r\n    \"knowledge_ids\": None,\r\n    \"nickname\": \"\",\r\n    \"temperature\": 0,\r\n    \"mark\": False,\r\n    \"backupChat\": False,\r\n    \"tipsText\": \"\",\r\n    \"chatMode\": 0,\r\n    \"isMulChat\": 2,\r\n    \"interaction\": \"{\\\"greet\\\":{\\\"hostess_mode\\\":True,\\\"welcome_wordlist\\\":[\\\"您好[称呼]，有什么可以帮您？\\\"],\\\"face_sourceid\\\":\\\"\\\"},\\\"revoke\\\":{\\\"wake_words\\\":\\\"你好小初\\\",\\\"covert_wake_words\\\":\\\"n ǐ h ǎo x iǎo ch ū @你好小初\\\"}}\"\r\n}"
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

