import logging
import pytest

from base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.dialog
class Test创建语音聊天对话(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_dialogs_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/add"
        headers = {"content-type": "application/json", "pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "name": "语音聊天_自动化接口测试",
            "machine_type": 4,
            "type": "",
            "scale": "9:16"
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["dialogs_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["dialogs_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_dialogs_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/edit"
        headers = {"content-type": "application/json", "pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "id": "{{dialogs_id}}",
            "name": "语音聊天_自动化接口测试",
            "type": "2d",
            "machine_type": 4,
            "agent_type": 1,
            "bot_id": "",
            "create_time": 1766541501,
            "update_time": 1766541501,
            "scale": "9:16",
            "human_id": 0,
            "voice_id": 1356,
            "background_id": 0,
            "expand": "",
            "word_action": "",
            "word_ssml": "",
            "word": "",
            "cover_img": "",
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
            "interaction": "{\"greet\":{\"hostess_mode\":True,\"welcome_wordlist\":[\"您好[称呼]，有什么可以帮您？\"],\"face_sourceid\":\"\"},\"revoke\":{\"wake_words\":\"你好小初\",\"covert_wake_words\":\"n ǐ h ǎo x iǎo ch ū @你好小初\"}}",
            "actionType": 0,
            "prompt": "",
            "appConfig": "{\"profile\":{\"avatar\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/48ddcaae-f90e-49cd-bcb8-ea6fbb85dc0b.png\",\"description\":\"你好，这是在做自动化接口测试\"},\"mode\":{\"guideMode\":True,\"spotDistance\":50}}"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_channel_create(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/channel/create"
        headers = {"content-type": "application/json", "pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "dialogId": "{{dialogs_id}}",
            "channelUserAccount": "jiaxiaomei"
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"
        assert extract_json_path(response.json(), "$.msg") == "Success", f"Expected msg=Success, got {response.text[:200]}"
        assert extract_json_path(response.json(), "$.data.channelInfo.status") == 1, f"Expected channelInfo.status=1, got {response.text[:200]}"

    def test_step_05_post_dialogs_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/dialogs/delete"
        headers = {"content-type": "application/json", "pragma": "no-cache", "priority": "u=1, i"}
        body = {"id": ["{{dialogs_id}}"]}
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"