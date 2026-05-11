import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

import pytest

from .base_test import BaseTest
from config import BASE_URL

logger = logging.getLogger("api_test")


@pytest.mark.ai
class TestAi配音接口测试(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "ssml": '<speak voice="zhistella" voice_id="1356"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>',
            "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
            "voice_id": 1356,
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        content_type = response.headers.get("Content-Type", "")
        assert "audio/wav" in content_type, f"Expected Content-Type to contain 'audio/wav', got '{content_type}'"

        content = response.content
        assert len(content) > 44, f"Expected audio content > 44 bytes (WAV header), got {len(content)} bytes"
        assert content[:4] == b'RIFF', f"Expected WAV file signature 'RIFF', got {content[:4]}"
        assert content[8:12] == b'WAVE', f"Expected WAV file signature 'WAVE', got {content[8:12]}"

    def test_step_03_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "ssml": '<speak voice="zh_male_tiancaitongsheng_mars_bigtts" voice_id="2297"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>',
            "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
            "voice_id": 2297,
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        content_type = response.headers.get("Content-Type", "")
        assert "audio/wav" in content_type, f"Expected Content-Type to contain 'audio/wav', got '{content_type}'"

        content = response.content
        assert len(content) > 44, f"Expected audio content > 44 bytes (WAV header), got {len(content)} bytes"
        assert content[:4] == b'RIFF', f"Expected WAV file signature 'RIFF', got {content[:4]}"
        assert content[8:12] == b'WAVE', f"Expected WAV file signature 'WAVE', got {content[8:12]}"

    def test_step_04_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "ssml": '<speak voice="S_JM0DTk1B1" voice_id="1440"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>',
            "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
            "voice_id": 1440,
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        content_type = response.headers.get("Content-Type", "")
        assert "audio/wav" in content_type, f"Expected Content-Type to contain 'audio/wav', got '{content_type}'"

        content = response.content
        assert len(content) > 44, f"Expected audio content > 44 bytes (WAV header), got {len(content)} bytes"
        assert content[:4] == b'RIFF', f"Expected WAV file signature 'RIFF', got {content[:4]}"
        assert content[8:12] == b'WAVE', f"Expected WAV file signature 'WAVE', got {content[8:12]}"

    def test_step_05_post_voice_audition(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voice/audition"
        headers = {"pragma": "no-cache", "priority": "u=1, i"}
        body = {
            "ssml": '<speak voice="mix_msvits_zhiyan_emo_16k" voice_id="2307"><s>水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。</s></speak>',
            "word": "水培养护需注重光照、温度、水质及根系管理。光照以散射光为主并避免阳光直射，不同植物需求各异：喜阴类需置于阴暗处，中性植物适应普通光照。温度宜保持在5-35℃，最佳水温为18-25℃左右，冬季需确保5℃以上防冻害，怕冷的植物如吊兰、绿萝等冬季需移入室内防冻伤。",
            "voice_id": 2307,
        }
        response = self._request("POST", url, json=body, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        content_type = response.headers.get("Content-Type", "")
        assert "audio/wav" in content_type, f"Expected Content-Type to contain 'audio/wav', got '{content_type}'"

        content = response.content
        assert len(content) > 44, f"Expected audio content > 44 bytes (WAV header), got {len(content)} bytes"
        assert content[:4] == b'RIFF', f"Expected WAV file signature 'RIFF', got {content[:4]}"
        assert content[8:12] == b'WAVE', f"Expected WAV file signature 'WAVE', got {content[8:12]}"