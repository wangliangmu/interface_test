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
class Test创建网页类型对话带动作(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "name": "网页_接口测试_带动作{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
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

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        body = {
            "id": "{{dialogs_id}}",
            "name": "网页_接口测试_带动作{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 1,
            "agent_type": 1,
            "bot_id": "",
            "create_time": 1778128238,
            "update_time": 1778128381,
            "scale": "16:9",
            "human_id": 2654,
            "voice_id": 0,
            "expand": '{"bg":{"size":{"width":1920,"height":1080}},"human":{"position":{"x":660,"y":7},"scale":{"x":1,"y":1},"size":{"width":600,"height":1067},"source":{"id":2654,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png"}},"page":[{"id":"[drag]-human","source":{"id":2654,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png"},"style":{"height":1067,"scaleX":1,"scaleY":1,"width":600,"x":660,"y":7,"zIndex":1},"type":"Human","visible":true}],"voice":{},"actionMap":{"broadCast":[449,448]},"interrupted_video":["https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123306_216eadd8f9.flv","https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123433_ae2558738f.flv","https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/interrupted/20260507123515_885e4ac9d0.flv"],"output_size":{"width":1920,"height":1080}}',
            "word_action": "",
            "word_ssml": "",
            "word": "",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/e3cfc2fe-a01b-49a7-9a80-4060184c3e04.jpeg",
            "speak_rate": 0,
            "qa_id": 0,
            "bg_path": "",
            "bc_path": "",
            "status": "success",
            "reason": "",
            "is_default": 2,
            "style": 0,
            "knowledge_ids": None,
            "nickname": "",
            "temperature": 0,
            "mark": False,
            "backupChat": False,
            "tipsText": "",
            "chatMode": 1,
            "isMulChat": 0,
            "actionType": 0,
            "prompt": "",
            "difyBotId": "",
            "interaction": '{"greet":{"hostess_mode":true,"welcome_wordlist":["您好[称呼]，有什么可以帮您？"],"face_sourceid":""},"revoke":{"wake_words":"你好小初","covert_wake_words":"n ǐ h ǎo x iǎo ch ū @你好小初"},"hotword":{"hotword_sourceid":""}}',
            "appConfig": "{}",
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_dialogs_get(self):
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
