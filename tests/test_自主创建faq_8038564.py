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


class Test自主创建faq:
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

    def test_step_02_post_knowledge_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "接口测试"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["qa_kn_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["qa_kn_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "question": "你好",
    "answer": "你好",
    "path": "",
    "type": "text",
    "base_id": "{{qa_kn_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "question": "插入图片",
    "answer": "这是一张图片。![img](https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/668cd89b-dcdf-4073-b941-55f1a0d0252c.png)",
    "path": "",
    "type": "text",
    "base_id": "{{qa_kn_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "question": "插入视频",
    "answer": "20240626154221_7ab6410bda.mp4",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/4ffff6b9-02de-4014-bb0d-7a3e13004508.mp4",
    "type": "video",
    "base_id": "{{qa_kn_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_06_get_excelfile_getdownloadUrl(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/excelfile/getdownloadUrl"
        url = resolve_template(url, self.context)
        headers = {
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        response = self.session.request(
            method="GET",
            url=url,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_07_post_excelfile_import(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/excelfile/import"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "base_id": "{{qa_kn_id}}",
    "filepath": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/34ab9c20-4c68-43d9-9d25-c0f96e8a472a.xlsx"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_08_post_qa_list(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/list"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "page_size": 10,
    "page": 1,
    "base_id": "{{qa_kn_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_09_post_knowledge_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/delete"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i",
    "token": "",
    "Authorization": ""
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": "{{qa_kn_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

