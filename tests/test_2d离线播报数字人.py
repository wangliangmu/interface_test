import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

class Test2d离线播报数字人:
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

    def test_step_02_post_draft_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/draft/edit"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "create": True,
    "create_name": "数字人播报{{$date.now|format('MMdd_HHmm')}}",
    "radio": "1080P",
    "mime": "MP4",
    "id": 4311,
    "page": 0,
    "name": "数字人播报{{$date.now|format('MMdd_HHmm')}}",
    "scenes": [
        {
            "voice_id": 1440,
            "bg_id": 7880,
            "human_id": 2654,
            "expand": "{\"bg\":{\"size\":{\"width\":1920,\"height\":1080},\"source\":{\"id\":7880,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png\"}},\"human\":{\"source\":{\"id\":2654,\"path\":\"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png\"},\"size\":{\"width\":743,\"height\":1321},\"position\":{\"x\":589,\"y\":-66},\"scale\":{\"x\":1,\"y\":1}},\"voice\":{\"source\":{\"id\":1440,\"name\":\"S_JM0DTk1B1\"}},\"output_size\":{\"width\":1920,\"height\":1080}}",
            "word": "柳州城市职业学院的先生与诸位同窗，可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。",
            "ssml": "<speak voice=\"S_JM0DTk1B1\" voice_id=\"1440\"><s>柳州城市职业学院的先生与诸位同窗，<action id=\"445\" name=\"左挥手\" duration=\"3.0s\" />可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，<action id=\"446\" name=\"开心\" duration=\"4.5s\" />心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，<action id=\"442\" name=\"右手介绍\" duration=\"4.0s\" />何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，<action id=\"443\" name=\"倾听\" duration=\"5.5s\" />也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。</s></speak>",
            "action": "柳州城市职业学院的先生与诸位同窗，<action id=\"445\" name=\"左挥手\" duration=\"3.0s\" />可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，<action id=\"446\" name=\"开心\" duration=\"4.5s\" />心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，<action id=\"442\" name=\"右手介绍\" duration=\"4.0s\" />何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，<action id=\"443\" name=\"倾听\" duration=\"5.5s\" />也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/aa14936b-025f-4ef6-8670-17848ef9f077.png",
            "stage": {
                "bg": {
                    "size": {
                        "width": 1920,
                        "height": 1080
                    },
                    "source": {
                        "id": 7880,
                        "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png"
                    }
                },
                "human": {
                    "source": {
                        "id": 2654,
                        "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png"
                    },
                    "size": {
                        "width": 743,
                        "height": 1321
                    },
                    "position": {
                        "x": 589,
                        "y": -66
                    },
                    "scale": {
                        "x": 1,
                        "y": 1
                    }
                },
                "voice": {
                    "source": {
                        "id": 1440,
                        "name": "S_JM0DTk1B1"
                    }
                }
            },
            "stage2": {
                "bg": {
                    "size": {
                        "width": 1920,
                        "height": 1080
                    },
                    "source": {
                        "id": 7880,
                        "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png"
                    }
                },
                "human": {
                    "source": {
                        "id": 2654,
                        "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png"
                    },
                    "size": {
                        "width": 743,
                        "height": 1321
                    },
                    "position": {
                        "x": 589,
                        "y": -66
                    },
                    "scale": {
                        "x": 1,
                        "y": 1
                    }
                },
                "voice": {
                    "source": {
                        "id": 1440,
                        "name": "S_JM0DTk1B1"
                    }
                }
            },
            "countError": False
        }
    ],
    "type": "broadcast",
    "scale": "16:9",
    "create_time": 1761101377,
    "update_time": 1772233947,
    "creator": "auto_test_jxm",
    "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/aa14936b-025f-4ef6-8670-17848ef9f077.png"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["composition_id"] = extract_json_path(response.json(), "$.data.composition_id")
        except Exception:
            self.context["composition_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_video_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/compose/video/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "video_id": "{{composition_id}}"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

