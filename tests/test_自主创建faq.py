import logging
import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.ai
class Test自主创建faq(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_knowledge_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {"name": "接口测试{{$date.now|format('MMdd_HHmm')}}"}
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["qa_kn_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["qa_kn_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "question": "你好",
            "answer": "你好",
            "path": "",
            "type": "text",
            "base_id": "{{qa_kn_id}}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.id") is not None, f"Expected $.data.id to exist, got {response.text[:200]}"

    def test_step_04_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "question": "插入图片",
            "answer": "这是一张图片。![img](https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/668cd89b-dcdf-4073-b941-55f1a0d0252c.png)",
            "path": "",
            "type": "text",
            "base_id": "{{qa_kn_id}}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.id") is not None, f"Expected $.data.id to exist, got {response.text[:200]}"

    def test_step_05_post_qa_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "question": "插入视频",
            "answer": "20240626154221_7ab6410bda.mp4",
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/4ffff6b9-02de-4014-bb0d-7a3e13004508.mp4",
            "type": "video",
            "base_id": "{{qa_kn_id}}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.id") is not None, f"Expected $.data.id to exist, got {response.text[:200]}"

    def test_step_06_get_excelfile_getdownloadUrl(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/excelfile/getdownloadUrl"
        headers = {"priority": "u=1, i"}
        response = self._request("GET", url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.msg") == "Success", f"Expected $.msg=Success, got {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.url") is not None, f"Expected $.data.url to exist, got {response.text[:200]}"

    def test_step_07_post_excelfile_import(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/excelfile/import"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "base_id": "{{qa_kn_id}}",
            "filepath": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/34ab9c20-4c68-43d9-9d25-c0f96e8a472a.xlsx"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.msg") == "Success", f"Expected $.msg=Success, got {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.total") == 6, f"Expected $.data.total=6, got {response.text[:200]}"

    def test_step_08_post_qa_list(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/qa/list"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "page_size": 10,
            "page": 1,
            "base_id": "{{qa_kn_id}}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.total") == 9, f"Expected $.data.total=9, got {response.text[:200]}"

    def test_step_09_post_knowledge_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/knowledge/delete"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {"id": "{{qa_kn_id}}"}
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"