import logging
import time

import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.dialog
class Test创建终端类型对话(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"priority": "u=1, i"}
        body = {
            "name": "终端_接口测试{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 2,
            "scale": "9:16",
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
            logger.info(f"创建对话成功，对话ID: {self.context['dialogs_id']}")
        except Exception:
            self.context["dialogs_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"priority": "u=1, i"}
        body = {
            "id": "{{dialogs_id}}",
            "name": "终端_接口测试{{$date.now|format('MMdd_HHmm')}}",
            "type": "2d",
            "machine_type": 2,
            "agent_type": 1,
            "bot_id": "",
            "create_time": 1764829391,
            "update_time": 1764829391,
            "scale": "9:16",
            "human_id": 3726,
            "background_id": 7850,
            "expand": '{"bg":{"size":{"width":1080,"height":1920},"source":{"id":7850,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/46f18c65-9135-437f-ba0a-779d4a5365e0.png"}},"human":{"position":{"x":-10,"y":30},"scale":{"x":1,"y":1},"size":{"width":1081,"height":1922},"source":{"id":3726,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/小初.png"}},"page":[{"id":"[drag]-dialogue","type":"Dialogue","style":{"width":984,"height":384,"x":48,"y":790,"zIndex":2,"scaleX":1,"scaleY":1,"rotate":0,"_userBg":"#006AFF","_userColor":"#fff","_robotBg":"#FFFFFF","_robotColor":"#222222","_Type":"vertical"}},{"id":"[drag]-hotRequest","type":"HotRequest","style":{"width":764,"height":80,"x":48,"y":124,"zIndex":2,"backgroundColor":"rgba(26, 26, 26, 0.5)","color":"#FFFFFF","_Type":"horizontal"}},{"id":"[drag]-wifiStatus","type":"WifiStatus","visible":true,"style":{"width":36,"height":36,"x":832,"y":48,"zIndex":2,"color":"#FFFFFF"}},{"id":"[drag]-timeStatus","type":"TimeStatus","visible":true,"style":{"width":180,"height":36,"x":876,"y":48,"zIndex":2,"color":"#FFFFFF"}},{"id":"[drag]-camera","type":"Camera","style":{"width":210,"height":274,"x":822,"y":124,"zIndex":2,"_tipColor":"#000000","_tipBgColor":"#FFFFFF"}},{"id":"[drag]-humanStatus","type":"HumanStatus","visible":true,"style":{"width":272,"height":84,"x":404,"y":20,"zIndex":2,"color":"#FFFFFF","backgroundColor":"rgba(51, 51, 51, 0.7)"},"source":{"path":"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_listen.png"}},{"id":"[drag]-image-logo","type":"Image","renderType":"image","style":{"width":176,"height":40,"x":48,"y":48,"zIndex":101},"source":{"path":"https://taichu-publish-data.wair.ac.cn/metaman-web/create/images/temp_logo_dark2.png"}},{"id":"[drag]-changeBtn","type":"ChangeBtn","style":{"width":100,"height":96,"x":932,"y":410,"zIndex":2,"backgroundColor":"rgba(26, 26, 26, 0.5)","color":"#FFFFFF","_iconColor":"#FFFFFF"}},{"id":"[drag]-quitBtn","type":"QuitBtn","style":{"width":100,"height":96,"x":932,"y":520,"zIndex":2,"backgroundColor":"rgba(26, 26, 26, 0.5)","color":"#FFFFFF","_iconColor":"#FFFFFF"}},{"id":"[drag]-volumeBtn","type":"VolumeBtn","style":{"width":60,"height":60,"x":960,"y":1780,"zIndex":2,"color":"#FFFFFF","backgroundColor":"rgba(26, 26, 26, 0.5)","_iconColor":"#FFFFFF"}},{"id":"[drag]-inputBtn","type":"InputBtn","style":{"width":60,"height":60,"x":960,"y":1700,"zIndex":2,"color":"#FFFFFF","backgroundColor":"rgba(26, 26, 26, 0.5)","_iconColor":"#FFFFFF"}},{"id":"[drag]-microphoneBtn","type":"MicrophoneBtn","style":{"width":60,"height":60,"x":960,"y":1620,"zIndex":2,"color":"#FFFFFF","backgroundColor":"rgba(26, 26, 26, 0.5)","_iconColor":"#FFFFFF"}}],"screenOrientation":1}',
            "word_action": "",
            "word_ssml": "",
            "word": "",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/45804bb0-5ab0-406a-9ae9-23b1dd824bfe.jpeg",
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