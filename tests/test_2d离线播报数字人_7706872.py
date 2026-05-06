import pytest
import requests
import json
import time

from .utils import resolve_template, resolve_dict, extract_json_path
from .config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG


import pytest
import requests
import json
import re
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "https://metahuman-prod.wair.ac.cn"
COMMON_HEADERS = [
    {
        "name": "token",
        "value": "{{token}}",
        "enable": True
    },
    {
        "name": "Authorization",
        "value": "Bearer {{token}}",
        "enable": True
    },
    {
        "name": "auto-gen-qa-tasks_id",
        "value": "{{auto-gen-qa-tasks_id}}",
        "enable": True
    }
]


def resolve_template(text, context):
    if not isinstance(text, str):
        return text
    def replacer(match):
        var_name = match.group(1)
        if var_name.startswith("$date"):
            beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
            return beijing_time.strftime("%m%d_%H%M")
        if var_name in context:
            return str(context[var_name])
        return match.group(0)
    return re.sub(r'\{\{(\S+?)\}\}', replacer, text)


def resolve_dict(d, context):
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            if isinstance(v, str):
                import re
                match = re.search(r'\{\{(\w+)\}\}', v)
                if match:
                    var_name = match.group(1)
                    result[k] = context.get(var_name, v)
                else:
                    result[k] = resolve_template(v, context)
            else:
                result[k] = resolve_dict(v, context)
        return result
    elif isinstance(d, list):
        return [resolve_dict(v, context) for v in d]
    elif isinstance(d, str):
        return resolve_template(d, context)
    return d


def extract_json_path(data, path):
    import jsonpath_ng
    expr = jsonpath_ng.parse(path)
    matches = expr.find(data)
    if matches:
        return matches[0].value
    return None


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
    "create_name": "接口测试",
    "radio": "1080P",
    "mime": "MP4",
    "id": 4311,
    "page": 0,
    "name": "接口测试",
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

    def test_step_05_post_video_delete(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/compose/video/delete"
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

