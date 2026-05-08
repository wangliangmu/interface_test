import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.clone
class Test3d形象生成(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_human_photo_3d_gen(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/photo_3d_gen"
        body = {
            "name": "3D形象{{$date.now|format('MMdd_HHmm')}}",
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/1a30a0d5-8ded-4bd7-8209-9f9b3bccb8ea.png",
            "sex": "女",
            "server_type": "img2img",
        }
        response = self._request("POST", url, json=body)
        try:
            self.context["3d_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建3D形象任务成功，任务ID: {self.context['3d_id']}")
        except Exception:
            self.context["3d_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {"human_id": "{{3d_id}}"}

        max_retries = 22
        wait_interval = 30
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