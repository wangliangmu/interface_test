import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

import pytest

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.clone
class Test精品克隆音频检测接口测试(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_voiceclone_checkwer(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/checkwer"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/b4b3ce5f-aad7-4090-ac45-82f3160830d8.m4a",
            "promptId": 7,
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            result = extract_json_path(response_json, "$.data.result")
            assert result == "音频识别合格", f"期望结果 '音频识别合格'，实际结果 '{result}': {response.text[:200]}"

            asr_rec = extract_json_path(response_json, "$.data.asr.asr_rec")
            expected_asr_keywords = [
                "你更喜欢喝咖啡吗",
                "我的口味",
                "平时喝茶",
                "给我推荐",
                "好喝的咖啡"
            ]
            
            for keyword in expected_asr_keywords:
                assert keyword in asr_rec, f"asr_rec 缺少关键词 '{keyword}': 实际内容 '{asr_rec}'"
                
        except Exception as e:
            assert False, f"解析响应或检查断言失败: {e}"