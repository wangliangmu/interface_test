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


@pytest.mark.smoke
@pytest.mark.clone
class Test2d视频克隆数字人(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_human_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/add"
        headers = {"priority": "u=1, i"}
        body = {
            "name": "2D视频{{$date.now|format('MMdd_HHmm')}}",
            "type": 3,
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/cb35e531-63e4-4ff4-bb19-74e5dca0adcc.mp4",
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["video_clone_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建视频克隆任务成功，任务ID: {self.context['video_clone_id']}")
        except Exception:
            self.context["video_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        headers = {"priority": "u=1, i"}
        body = {"human_id": "{{video_clone_id}}"}

        max_retries = 15
        wait_interval = 60
        response = None

        for attempt in range(max_retries):
            response = self._request("POST", url, json=body, headers=headers)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

            try:
                response_json = response.json()
                status = extract_json_path(response_json, "$.data.status")

                if status is None:
                    logger.error(f"无法提取 status 字段，响应: {response.text[:500]}")
                    pytest.fail(f"无法提取 status 字段，响应: {response.text[:500]}")

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

    def test_step_04_post_human_list(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/list"
        headers = {"priority": "u=1, i"}
        body = {"page": 1, "page_size": 10, "org": 2, "type": 3}
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.status") == "normal", f"Expected status=normal, got {response.text[:200]}"