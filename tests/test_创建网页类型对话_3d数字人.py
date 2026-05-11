import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import pytest
import time

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.dialog
class Test创建网页类型对话3d数字人(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "name": "网页_3d数字人{{$date.now|format('MMdd_HHmm')}}",
            "type": "3d",
            "machine_type": 1,
            "scale": "16:9",
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["dialogs_id"] = None
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "id": "{{dialogs_id}}",
            "name": "网页_3d数字人{{$date.now|format('MMdd_HHmm')}}",
            "type": "3d",
            "machine_type": 1,
            "agent_type": 1,
            "bot_id": "",
            "create_time": 1764813728,
            "update_time": 1764813728,
            "scale": "16:9",
            "human_id": 3756,
            "background_id": 7809,
            "expand": '{"bg":{"source":{"id":7809,"path":"https://publish-data.oss-cn-wuhan-lr.aliyuncs.com:443/metaman/bg_image/177/4d559d5b-b86d-412a-96d0-a270e8d9a679.png"},"size":{"width":1920,"height":1080}},"human":{"position":{"x":660,"y":7},"scale":{"x":1,"y":1},"size":{"width":600,"height":1067},"source":{"id":3756,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/177/afd80d18-c1a4-4a41-b204-d8d119b8e15b.png"}},"page":[{"id":"[drag]-human","type":"Human","visible":true,"style":{"x":660,"y":7,"scaleX":1,"scaleY":1,"width":600,"height":1067,"zIndex":1},"source":{"id":3756,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/177/afd80d18-c1a4-4a41-b204-d8d119b8e15b.png"}}],"voice":{},"actionMap":{}}',
            "word_action": "",
            "word_ssml": "",
            "word": "",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/1e7f1c6b-51b0-429a-9de5-0ac2558ea333.jpeg",
            "speak_rate": 0,
            "qa_id": 0,
            "bg_path": "",
            "bc_path": "",
            "status": "normal",
            "reason": "",
            "is_default": 2,
            "style": 0,
            "knowledge_ids": None,
            "nickname": "",
            "temperature": 0,
            "mark": False,
            "backupChat": False,
            "tipsText": "",
            "chatMode": 0,
            "isMulChat": 0,
            "actionType": 0,
            "prompt": "",
            "interaction": '{"greet":{"hostess_mode":true,"welcome_wordlist":["您好[称呼]，有什么可以帮您？"],"face_sourceid":""},"revoke":{"wake_words":"你好小初","covert_wake_words":"n ǐ h ǎo x iǎo ch ū @你好小初"}}',
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_06_post_dialogs_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/get"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {"id": "{{dialogs_id}}"}

        max_retries = 18
        wait_interval = 30
        response = None

        for attempt in range(max_retries):
            response = self._request("POST", url, json=body, headers=headers)
            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

            try:
                response_json = response.json()
                status = extract_json_path(response_json, "$.data.status")

                if status is None:
                    logger.error(f"无法提取 status 字段，响应: {response.text[:500]}")
                    pytest.fail(f"无法提取 status 字段，响应: {response.text[:500]}")

                if status in ["success", "failed"]:
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
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.status")
            assert (
                status == "success"
            ), f"期望状态 'success'，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"
