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
        return {k: resolve_dict(v, context) for k, v in d.items()}
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


class Test图片克隆数字人:
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
    "priority": "u=1, i",
    "token": ""
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

    def test_step_02_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        url = resolve_template(url, self.context)
        headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjExMjQwMDYsImlhdCI6MTc2MTAzNzYwNiwiand0VXNlcklkIjoyMzN9.jarPwDQg_Jv6k_UBami_ubSbnBtTwi7ytu-NBf_j8Po",
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": "",
    "auto-gen-qa-tasks_id": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/aa7a0211-9b17-4938-ae39-c76831d240b5.jpg",
    "type": "image"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_human_getAlphaPhoto(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/getAlphaPhoto"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": "",
    "auto-gen-qa-tasks_id": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/aa7a0211-9b17-4938-ae39-c76831d240b5.jpg"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_photoClone(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/photoClone"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": "",
    "auto-gen-qa-tasks_id": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "自动化测试",
    "src_path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/aa7a0211-9b17-4938-ae39-c76831d240b5.jpg",
    "alpha_path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/339d5a43-e01a-4222-8706-40a7ca8f96a4.png",
    "bUsed": True
}
        body = resolve_dict(body, self.context)
        
        max_retries = 30
        wait_interval = 5
        poll_expression = "$.data.status"
        poll_expected = 'completed'
        
        for attempt in range(max_retries):
            response = self.session.request(
                method="POST",
                url=url,
                json=body,
                headers=headers,
            )
            if response.status_code == 200:
                try:
                    actual_value = extract_json_path(response.json(), poll_expression)
                    if actual_value == poll_expected:
                        break
                except Exception:
                    pass
            time.sleep(wait_interval)
        else:
            raise TimeoutError(f"Polling timeout after {max_retries * wait_interval} seconds")
        
        try:
            self.context["photo_clone_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["photo_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_06_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{photo_clone_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_07_post_human_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{photo_clone_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

