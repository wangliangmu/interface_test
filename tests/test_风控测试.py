import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import pytest

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.risk
class Test风控测试(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        headers = {
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
        }
        body = {
            "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/2055f570-ddfa-414f-a58b-ebec7d32797c.png",
            "type": "image",
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

        response_json = response.json()
        check_result = extract_json_path(response_json, "$.data.check_result")
        description = extract_json_path(response_json, "$.data.description")
        assert check_result is False, f"风险检查结果应为false，实际为: {check_result}"
        assert "涉政" in description, f"描述应包含'涉政'，实际为: {description}"

    def test_step_03_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        headers = {
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
        }
        body = {
            "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/0fef2de4-4328-4773-b267-e013d970b74c.mp4",
            "type": "video",
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

        response_json = response.json()
        check_result = extract_json_path(response_json, "$.data.check_result")
        description = extract_json_path(response_json, "$.data.description")
        assert check_result is False, f"风险检查结果应为false，实际为: {check_result}"
        assert "涉政" in description, f"描述应包含'涉政'，实际为: {description}"
