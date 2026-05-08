import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import time

import pytest

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.clone
class Test2d换脸克隆(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_human_faceSwap(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/faceSwap"
        body = {
            "name": "2D换脸{{$date.now|format('MMdd_HHmm')}}",
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/178/00abf0c3-c0ff-497f-ad4a-7da13799c927.jpg",
            "id": 3162,
        }
        response = self._request("POST", url, json=body)
        try:
                
            
            self.context["faceswap_task_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建换脸任务成功，任务ID: {self.context['faceswap_task_id']}")
        except Exception:
            self.context["faceswap_task_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        body = {"human_id": "{{faceswap_task_id}}"}

        max_retries = 15
        wait_interval = 60
        response = None

        for attempt in range(max_retries):
            response = self._request("POST", url, json=body)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

            try:
                response_json = response.json()

                status = extract_json_path(response_json, "$.data.status")

                if status in ["normal", "failed"]:
                    break
                elif status == "producing":
                    logger.info(f"状态为 'producing'，等待 {wait_interval} 秒...")
                    time.sleep(wait_interval)
                else:
                    logger.info(f"未知状态: {status}，继续轮询...")
                    time.sleep(wait_interval)
            except Exception as e:
                logger.error(f"解析状态失败: {e}")
                time.sleep(wait_interval)

        assert response is not None, "轮询后未收到响应"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.status")
            assert status == "normal", f"期望状态 'normal'，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"