import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.smoke
class Test首页接口测试(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_user_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/user/get"
        headers = {"priority": "u=1, i"}
        response = self._request("POST", url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_get_api_config(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/config"
        headers = {"priority": "u=1, i"}
        response = self._request("GET", url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_device_typeList(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/device/typeList"
        headers = {"priority": "u=1, i"}
        response = self._request("POST", url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_human_list(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/public/human/list"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "page": 1,
            "page_size": 12
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_06_post_dialogs_grant(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/grant"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {"id": 2327}
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"