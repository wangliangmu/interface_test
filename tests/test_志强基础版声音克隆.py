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
class Test志强基础版声音克隆(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_voiceclone_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/add"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "name": "测试1",
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/9756fa15-aca9-4dc6-b99a-3db855f3ceec.wav"
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["voice_clone_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建声音克隆任务成功，任务ID: {self.context['voice_clone_id']}")
        except Exception:
            self.context["voice_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_voiceclone_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/get"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {"id": "{{voice_clone_id}}"}

        max_retries = 30
        wait_interval = 20
        response = None

        for attempt in range(max_retries):
            try:
                response = self._request("POST", url, json=body, headers=headers)
                assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

                response_json = response.json()
                status = extract_json_path(response_json, "$.data.data.status")

                if status in ["normal", "failed"]:
                    break
                elif status == "producing":
                    logger.info(f"状态为 'producing'，等待 {wait_interval} 秒...")
                    time.sleep(wait_interval)
                else:
                    logger.info(f"未知状态: {status}，继续轮询...")
                    time.sleep(wait_interval)
            except Exception as e:
                logger.error(f"发生错误，继续下一次轮询: {e}")
                time.sleep(wait_interval)

        assert response is not None, "轮询后未收到响应"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.data.status")
            assert status == "normal", f"期望状态 'normal'，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"