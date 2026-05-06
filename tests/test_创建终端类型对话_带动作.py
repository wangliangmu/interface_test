import pytest
import requests
import json
import time

from .utils import resolve_template, resolve_dict, extract_json_path
from .config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG


import pytest
import requests
import json
import re
import time
from datetime import datetime, timezone, timedelta

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
            beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
            return beijing_time.strftime("%m%d_%H%M")
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


class Test创建终端类型对话带动作:
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
    "name": "终端_接口测试_带动作{{$date.now|format('MMdd_HHmm')}}",
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
    "_raw": "{\r\n    \"id\": {{dialogs_id}},\r\n    \"name\": \"终端_接口测试_带动作DATE_FORMAT_PLACEHOLDER\",\r\n    \"type\": \"2d\",\r\n    \"machine_type\": 2,\r\n    \"agent_type\": 1,\r\n    \"bot_id\": \"\",\r\n    \"create_time\": 1761287963,\r\n    \"update_time\": 1761287963,\r\n    \"scale\": \"9:16\",\r\n    \"human_id\": 2654,\r\n    \"voice_id\": 1440,\r\n    \"background_id\": 7850,\r\n    \"expand\": \"{\\\"bg\\\":{\\\"size\\\":{\\\"height\\\":1920,\\\"width\\\":1080},\\\"source\\\":{\\\"id\\\":7850,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/46f18c65-9135-437f-ba0a-779d4a5365e0.png\\\"}},\\\"human\\\":{\\\"position\\\":{\\\"x\\\":-56,\\\"y\\\":-160},\\\"scale\\\":{\\\"x\\\":1,\\\"y\\\":1},\\\"size\\\":{\\\"width\\\":1173,\\\"height\\\":2085},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}},\\\"page\\\":[{\\\"id\\\":\\\"[drag]-dialogue\\\",\\\"type\\\":\\\"Dialogue\\\",\\\"style\\\":{\\\"width\\\":984,\\\"height\\\":384,\\\"x\\\":48,\\\"y\\\":790,\\\"zIndex\\\":2,\\\"scaleX\\\":1,\\\"scaleY\\\":1,\\\"rotate\\\":0,\\\"_userBg\\\":\\\"#006AFF\\\",\\\"_userColor\\\":\\\"#fff\\\",\\\"_robotBg\\\":\\\"#FFFFFF\\\",\\\"_robotColor\\\":\\\"#222222\\\"}},{\\\"id\\\":\\\"[drag]-hotRequest\\\",\\\"type\\\":\\\"HotRequest\\\",\\\"style\\\":{\\\"width\\\":764,\\\"height\\\":80,\\\"x\\\":48,\\\"y\\\":124,\\\"zIndex\\\":2,\\\"backgroundColor\\\":\\\"rgba(26, 26, 26, 0.5)\\\",\\\"color\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-wifiStatus\\\",\\\"type\\\":\\\"WifiStatus\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"width\\\":36,\\\"height\\\":36,\\\"x\\\":832,\\\"y\\\":48,\\\"zIndex\\\":2,\\\"color\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-timeStatus\\\",\\\"type\\\":\\\"TimeStatus\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"width\\\":180,\\\"height\\\":36,\\\"x\\\":876,\\\"y\\\":48,\\\"zIndex\\\":2,\\\"color\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-camera\\\",\\\"type\\\":\\\"Camera\\\",\\\"style\\\":{\\\"width\\\":210,\\\"height\\\":274,\\\"x\\\":822,\\\"y\\\":124,\\\"zIndex\\\":2,\\\"_tipColor\\\":\\\"#000000\\\",\\\"_tipBgColor\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-humanStatus\\\",\\\"type\\\":\\\"HumanStatus\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"width\\\":272,\\\"height\\\":84,\\\"x\\\":404,\\\"y\\\":20,\\\"zIndex\\\":2,\\\"color\\\":\\\"#FFFFFF\\\",\\\"backgroundColor\\\":\\\"rgba(51, 51, 51, 0.7)\\\"},\\\"source\\\":{\\\"path\\\":\\\"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_listen.png\\\"}},{\\\"id\\\":\\\"[drag]-image-logo\\\",\\\"type\\\":\\\"Image\\\",\\\"renderType\\\":\\\"image\\\",\\\"style\\\":{\\\"width\\\":176,\\\"height\\\":40,\\\"x\\\":48,\\\"y\\\":48,\\\"zIndex\\\":101},\\\"source\\\":{\\\"path\\\":\\\"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_logo_dark2.png\\\"}},{\\\"id\\\":\\\"[drag]-changeBtn\\\",\\\"type\\\":\\\"ChangeBtn\\\",\\\"style\\\":{\\\"width\\\":100,\\\"height\\\":96,\\\"x\\\":932,\\\"y\\\":410,\\\"zIndex\\\":2,\\\"backgroundColor\\\":\\\"rgba(26, 26, 26, 0.5)\\\",\\\"color\\\":\\\"#FFFFFF\\\",\\\"_iconColor\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-quitBtn\\\",\\\"type\\\":\\\"QuitBtn\\\",\\\"style\\\":{\\\"width\\\":100,\\\"height\\\":96,\\\"x\\\":820,\\\"y\\\":410,\\\"zIndex\\\":2,\\\"backgroundColor\\\":\\\"rgba(26, 26, 26, 0.5)\\\",\\\"color\\\":\\\"#FFFFFF\\\",\\\"_iconColor\\\":\\\"#FFFFFF\\\"}},{\\\"id\\\":\\\"[drag]-human\\\",\\\"type\\\":\\\"Human\\\",\\\"style\\\":{\\\"x\\\":-56,\\\"y\\\":-160,\\\"scaleX\\\":1,\\\"scaleY\\\":1,\\\"width\\\":1173,\\\"height\\\":2085,\\\"zIndex\\\":1},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}}],\\\"voice\\\":{\\\"source\\\":{\\\"id\\\":1440,\\\"name\\\":\\\"S_JM0DTk1B1\\\"}},\\\"actionMap\\\":{\\\"awake\\\":[326],\\\"broadCast\\\":[326,387,385],\\\"knowledgeSearch\\\":[387],\\\"internetSearch\\\":[387]}}\",\r\n    \"word_action\": \"\",\r\n    \"word_ssml\": \"\",\r\n    \"word\": \"\",\r\n    \"cover_img\": \"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/da95b944-4a45-411c-8b7c-f496893508a2.jpeg\",\r\n    \"speak_rate\": 0,\r\n    \"qa_id\": 0,\r\n    \"bg_path\": \"\",\r\n    \"bc_path\": \"\",\r\n    \"status\": \"normal\",\r\n    \"reason\": \"\",\r\n    \"is_default\": 2,\r\n    \"style\": 0,\r\n    \"knowledge_ids\": None,\r\n    \"nickname\": \"\",\r\n    \"temperature\": 0,\r\n    \"mark\": False,\r\n    \"backupChat\": False,\r\n    \"tipsText\": \"\",\r\n    \"chatMode\": 0,\r\n    \"isMulChat\": 0,\r\n    \"interaction\": \"{\\\"greet\\\":{\\\"hostess_mode\\\":True,\\\"welcome_wordlist\\\":[\\\"您好[称呼]，有什么可以帮您？\\\"],\\\"face_sourceid\\\":\\\"\\\"},\\\"revoke\\\":{\\\"wake_words\\\":\\\"你好小初\\\",\\\"covert_wake_words\\\":\\\"n ǐ h ǎo x iǎo ch ū @你好小初\\\"}}\"\r\n}"
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

