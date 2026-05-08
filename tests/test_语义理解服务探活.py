import logging
import pytest

from base_test import BaseTest
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.ai
class Test语义理解服务探活(BaseTest):
    def test_step_01_post_infer_11120(self):
        url = "https://platform-h20.wair.ac.cn/api/v1/infer/11120"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiJ9.j6-hUMaFYdSIzfc6i6TJ5DaS96Z9I78SrjxAOg-71yE"
        }
        body = {
            "query": "切换数字人",
            "base_id": 10000
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.top_base_id") == 10000, f"Expected top_base_id=10000, got {response.text[:200]}"
        assert extract_json_path(response.json(), "$.status_message") == "ok", f"Expected status_message=ok, got {response.text[:200]}"