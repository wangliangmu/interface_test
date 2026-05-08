import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.ai
class TestAi职业照接口测试(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_img2img_checktext(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/ai/img2img/checktext"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {"prompt": "医生"}
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_img2img_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/ai/img2img/add"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "prompt": "医生",
            "resolution": "1382x1382",
            "server_type": "img2img",
            "url": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/8499971e-d6b6-46d6-9350-d28b76b84985.png",
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["img2img_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建AI职业照任务成功，任务ID: {self.context['img2img_id']}")
        except Exception:
            self.context["img2img_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_ai_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/ai/get"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {"id": "{{img2img_id}}"}

        wait_seconds = 60
        logger.info(f"等待 {wait_seconds} 秒进行AI职业照生成...")
        time.sleep(wait_seconds)

        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.status") == "success", f"Expected status=success, got {response.text[:200]}"