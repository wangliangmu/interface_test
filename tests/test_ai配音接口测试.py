import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.ai
class TestAi配音接口测试:
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
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "source": "show",
    "username": "auto_test_jxm",
    "password": "auto_test_jxm123",
    "permission": "on"
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
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_02_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "ssml": "<speak voice=\"zhistella\" voice_id=\"1356\"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>",
    "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
    "voice_id": 1356
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "ssml": "<speak voice=\"zh_male_tiancaitongsheng_mars_bigtts\" voice_id=\"2297\"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>",
    "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
    "voice_id": 2297
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "ssml": "<speak voice=\"S_JM0DTk1B1\" voice_id=\"1440\"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>",
    "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
    "voice_id": 1440
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_05_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "ssml": "<speak voice=\"mix_msvits_zhiyan_emo_16k\" voice_id=\"2307\"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>",
    "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
    "voice_id": 2307
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

