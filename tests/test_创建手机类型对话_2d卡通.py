import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.dialog
class Test创建手机类型对话2d卡通(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"priority": "u=1, i"}
        body = {
            "name": "手机_2D卡通{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 3,
            "scale": "9:16"
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建手机2D卡通对话成功，对话ID: {self.context['dialogs_id']}")
        except Exception:
            self.context["dialogs_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"priority": "u=1, i"}
        body = {
            "id": "{{dialogs_id}}",
            "name": "手机_2D卡通{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 3,
            "agent_type": 1,
            "bot_id": "",
            "create_time": 1776847245,
            "update_time": 1776847245,
            "scale": "9:16",
            "human_id": 4642,
            "voice_id": 0,
            "expand": "{\"bg\":{\"size\":{\"width\":1080,\"height\":1920}},\"human\":{\"position\":{\"x\":100,\"y\":178},\"scale\":{\"x\":1,\"y\":1},\"size\":{\"width\":880,\"height\":1564},\"source\":{\"id\":4642,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/background/cover/177/新春小马.png\"}},\"page\":[{\"id\":\"[drag]-human\",\"type\":\"Human\",\"visible\":true,\"style\":{\"x\":100,\"y\":178,\"scaleX\":1,\"scaleY\":1,\"width\":880,\"height\":1564,\"zIndex\":1},\"source\":{\"id\":4642,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/background/cover/177/新春小马.png\"}}],\"voice\":{},\"actionMap\":{},\"output_size\":{\"width\":1080,\"height\":1920}}",
            "word_action": "",
            "word_ssml": "",
            "word": "",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/184/bf1da2f1-1821-4c6a-97eb-0d03c64f1ddd.jpeg",
            "speak_rate": 0,
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
            "isMulChat": 2,
            "actionType": 0,
            "prompt": "",
            "difyBotId": "",
            "interaction": "{\"greet\":{\"hostess_mode\":true,\"welcome_wordlist\":[\"您好[称呼]，有什么可以帮您？\"],\"face_sourceid\":\"\"},\"revoke\":{\"wake_words\":\"你好小初\",\"covert_wake_words\":\"n ǐ h ǎo x iǎo ch ū @你好小初\"},\"hotword\":{\"hotword_sourceid\":\"\"}}",
            "appConfig": "{}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_dialogs_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/get"
        headers = {"priority": "u=1, i"}
        body = {"id": "{{dialogs_id}}"}

        max_retries = 18
        wait_interval = 30
        response = None

        for attempt in range(max_retries):
            response = self._request("POST", url, json=body, headers=headers)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

            try:
                response_json = response.json()
                status = extract_json_path(response_json, "$.data.data.status")

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
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.data.status")
            assert status == "success", f"期望状态 'success'，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"