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


class Test3d形象生成:
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

    def test_step_02_post_human_photo_3d_gen(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/photo_3d_gen"
        url = resolve_template(url, self.context)
        headers = {}
        body = {
    "name": "自动化接口测试",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/1a30a0d5-8ded-4bd7-8209-9f9b3bccb8ea.png",
    "sex": "女",
    "server_type": "img2img"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
        )
        try:
            self.context["3d_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["3d_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{3d_id}}"
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
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{3d_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

