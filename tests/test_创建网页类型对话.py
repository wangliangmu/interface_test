import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.dialog
class Test创建网页类型对话(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"priority": "u=1, i"}
        body = {
            "name": "网页_接口测试{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 1,
            "scale": "16:9"
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建网页对话成功，对话ID: {self.context['dialogs_id']}")
        except Exception:
            self.context["dialogs_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"priority": "u=1, i"}
        body = {
            "_raw": "{\"id\": {{dialogs_id}},\"name\": \"网页_接口测试{{$date.now|format('MMdd_HHmm')}}\",\"type\": \"2d\",\"machine_type\": 1,\"agent_type\": 1,\"bot_id\": \"\",\"create_time\": 1761113732,\"update_time\": 1761113732,\"scale\": \"16:9\",\"human_id\": 2654,\"voice_id\": 1440,\"expand\": \"{\\\"bg\\\":{\\\"size\\\":{\\\"width\\\":1920,\\\"height\\\":1080}},\\\"human\\\":{\\\"position\\\":{\\\"x\\\":660,\\\"y\\\":7},\\\"scale\\\":{\\\"x\\\":1,\\\"y\\\":1},\\\"size\\\":{\\\"width\\\":600,\\\"height\\\":1067},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}},\\\"page\\\":[{\\\"id\\\":\\\"[drag]-human\\\",\\\"type\\\":\\\"Human\\\",\\\"visible\\\":True,\\\"style\\\":{\\\"x\\\":660,\\\"y\\\":7,\\\"scaleX\\\":1,\\\"scaleY\\\":1,\\\"width\\\":600,\\\"height\\\":1067,\\\"zIndex\\\":1},\\\"source\\\":{\\\"id\\\":2654,\\\"path\\\":\\\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\\\"}}],\\\"voice\\\":{\\\"source\\\":{\\\"id\\\":1440,\\\"name\\\":\\\"S_JM0DTk1B1\\\"}},\\\"actionMap\\\":{\\\"broadCast\\\":[388]}}\",\"word_action\": \"\",\"word_ssml\": \"\",\"word\": \"你好，我是黛玉\",\"cover_img\": \"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/580a927f-5bd5-4243-bd4c-dbfc69bc0f13.jpeg\",\"speak_rate\": 0,\"bg_path\": \"\",\"bc_path\": \"\",\"status\": \"normal\",\"reason\": \"\",\"is_default\": 1,\"style\": 0,\"knowledge_ids\": null,\"nickname\": \"\",\"temperature\": 0,\"mark\": false,\"backupChat\": false,\"tipsText\": \"\",\"chatMode\": 0,\"isMulChat\": 2,\"interaction\": \"{\\\"greet\\\":{\\\"hostess_mode\\\":true,\\\"welcome_wordlist\\\":[\\\"您好[称呼]，有什么可以帮您？\\\"],\\\"face_sourceid\\\":\\\"\\\"},\\\"revoke\\\":{\\\"wake_words\\\":\\\"你好小初\\\",\\\"covert_wake_words\\\":\\\"n ǐ h ǎo x iǎo ch ū @你好小初\\\"}}\"}",
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