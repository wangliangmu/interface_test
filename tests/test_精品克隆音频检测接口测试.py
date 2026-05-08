import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG


@pytest.mark.clone
class Test精品克隆音频检测接口测试:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_post_account_login(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/account/login"
        url = resolve_template(url, self.context)
        headers = {"content-type": "application/json", "priority": "u=1, i"}
        headers = resolve_dict(headers, self.context)
        body = {
            "source": "show",
            "username": "auto_test_jxm",
            "password": "auto_test_jxm123",
            "permission": "on",
        }
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["token"] = extract_json_path(response.json(), "$.data.token")
        except Exception:
            self.context["token"] = None
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_02_post_voiceclone_checkwer(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/checkwer"
        url = resolve_template(url, self.context)
        headers = {
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
        }
        headers = resolve_dict(headers, self.context)
        body = {
            "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/b4b3ce5f-aad7-4090-ac45-82f3160830d8.m4a",
            "promptId": 7,
        }
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            result = extract_json_path(response_json, "$.data.result")
            assert (
                result == "音频识别合格"
            ), f"Expected result '音频识别合格', got '{result}': {response.text[:200]}"

            asr_rec = extract_json_path(response_json, "$.data.asr.asr_rec")
            expected_asr_rec = "你更喜欢喝咖啡吗？和我的口味不太一样。我平时喝茶多一些，你可以给我推荐一些好喝的咖啡吗？"
            assert (
                asr_rec == expected_asr_rec
            ), f"Expected asr_rec mismatch: {response.text[:200]}"
        except Exception as e:
            assert False, f"Failed to parse response or check assertions: {e}"
