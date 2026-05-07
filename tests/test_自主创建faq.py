import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.ai
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

    def test_step_02_post_knowledge_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "接口测试{{$date.now|format('MMdd_HHmm')}}"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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
    "priority": "u=1, i"
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

