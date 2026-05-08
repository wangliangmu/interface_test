import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.ai
class TestPpt讲解视频合成(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_14_compose(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/drafts/14/compose"
        body = {
            "id": 14,
            "name": "PPT视频{{$date.now|format('MMdd_HHmm')}}",
            "quality": "1080P",
            "format": "MP4",
        }
        response = self._request("POST", url, json=body)
        try:
            self.context["compose_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建PPT视频合成任务成功，任务ID: {self.context['compose_id']}")
        except Exception:
            self.context["compose_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_get_pptvideo_taskspage_size1page1typeppttask_typev(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/tasks?page_size=1&page=1&type=ppt&task_type=video_merge"
        headers = {"priority": "u=1, i"}

        max_retries = 36
        wait_interval = 10
        response = None

        for attempt in range(max_retries):
            try:
                response = self._request("GET", url, headers=headers)
                assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

                response_json = response.json()
                status = extract_json_path(response_json, "$.data.list[0].status")

                if status in [2, 3]:
                    break
                elif status == 1:
                    logger.info(f"状态为 1 (处理中)，等待 {wait_interval} 秒...")
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
            status = extract_json_path(response_json, "$.data.list[0].status")
            assert status == 2, f"期望状态 2 (成功)，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"

    def test_step_05_get_pptvideo_taskspage_size1page1typeppttask_typev(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/mammoth/v1/ppt-video/tasks?page_size=1&page=1&type=ppt&task_type=video_merge"
        headers = {"priority": "u=1, i"}
        response = self._request("GET", url, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.list[0].id") == self.context.get("compose_id"), f"Expected list[0].id={{compose_id}}, got {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.list[0].status") == 2, f"Expected list[0].status=2, got {response.text[:200]}"