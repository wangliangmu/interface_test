import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import time

import pytest

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.clone
class Test2d离线播报数字人(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()

    def test_step_02_post_draft_edit(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/draft/edit"
        headers = {"priority": "u=1, i"}
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
                    "expand": '{"bg":{"size":{"width":1920,"height":1080},"source":{"id":7880,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png"}},"human":{"source":{"id":2654,"path":"https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png"},"size":{"width":743,"height":1321},"position":{"x":589,"y":-66},"scale":{"x":1,"y":1}},"voice":{"source":{"id":1440,"name":"S_JM0DTk1B1"}},"output_size":{"width":1920,"height":1080}}',
                    "word": "柳州城市职业学院的先生与诸位同窗，可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。",
                    "ssml": '<speak voice="S_JM0DTk1B1" voice_id="1440"><s>柳州城市职业学院的先生与诸位同窗，<action id="445" name="左挥手" duration="3.0s" />可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，<action id="446" name="开心" duration="4.5s" />心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，<action id="442" name="右手介绍" duration="4.0s" />何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，<action id="443" name="倾听" duration="5.5s" />也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。</s></speak>',
                    "action": '柳州城市职业学院的先生与诸位同窗，<action id="445" name="左挥手" duration="3.0s" />可都安好？说起来倒要谢过紫东太初那多模态大模型，竟叫我跨越了古今时光，得以与诸君相见，<action id="446" name="开心" duration="4.5s" />心中实是欢喜得紧呢！如今这人工智能的时代浪潮正盛，恰似那东风拂过百花洲，诸君正值风华年少，<action id="442" name="右手介绍" duration="4.0s" />何不趁这好时节牢牢抓住机遇？若能在学问上奋力创新，将来定能为这世道创些实实在在的财富，<action id="443" name="倾听" duration="5.5s" />也好为家国尽一份心力 —— 这般志向，想来倒是比那枝头的春光更叫人欣悦呢。',
                    "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/aa14936b-025f-4ef6-8670-17848ef9f077.png",
                    "stage": {
                        "bg": {
                            "size": {"width": 1920, "height": 1080},
                            "source": {
                                "id": 7880,
                                "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png",
                            },
                        },
                        "human": {
                            "source": {
                                "id": 2654,
                                "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png",
                            },
                            "size": {"width": 743, "height": 1321},
                            "position": {"x": 589, "y": -66},
                            "scale": {"x": 1, "y": 1},
                        },
                        "voice": {"source": {"id": 1440, "name": "S_JM0DTk1B1"}},
                    },
                    "stage2": {
                        "bg": {
                            "size": {"width": 1920, "height": 1080},
                            "source": {
                                "id": 7880,
                                "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/bg_image/177/9f3162a0-3b7a-486c-a5af-72921eaf937d.png",
                            },
                        },
                        "human": {
                            "source": {
                                "id": 2654,
                                "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/origin/177/黛玉.png",
                            },
                            "size": {"width": 743, "height": 1321},
                            "position": {"x": 589, "y": -66},
                            "scale": {"x": 1, "y": 1},
                        },
                        "voice": {"source": {"id": 1440, "name": "S_JM0DTk1B1"}},
                    },
                    "countError": False,
                }
            ],
            "type": "broadcast",
            "scale": "16:9",
            "create_time": 1761101377,
            "update_time": 1772233947,
            "creator": "auto_test_jxm",
            "cover_img": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/image/233/aa14936b-025f-4ef6-8670-17848ef9f077.png",
        }
        response = self._request("POST", url, json=body, headers=headers)
        try:
            self.context["composition_id"] = extract_json_path(response.json(), "$.data.composition_id")
            logger.info(f"创建数字人播报任务成功，任务ID: {self.context['composition_id']}")
        except Exception:
            self.context["composition_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_video_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/compose/video/get"
        headers = {"priority": "u=1, i"}
        body = {"video_id": "{{composition_id}}"}

        max_retries = 15
        wait_interval = 60
        response = None

        for attempt in range(max_retries):
            try:
                response = self._request("POST", url, json=body, headers=headers)
                assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

                response_json = response.json()
                status = extract_json_path(response_json, "$.data.status")

                if status in ["normal", "failed"]:
                    break
                elif status == "producing":
                    logger.info(f"状态为 'producing'，等待 {wait_interval} 秒...")
                    time.sleep(wait_interval)
                else:
                    logger.info(f"未知状态: {status}，继续轮询...")
                    time.sleep(wait_interval)
            except Exception as e:
                logger.error(f"发生错误，继续下一次轮询: {e}")
                time.sleep(wait_interval)

        assert response is not None, "轮询后未收到响应"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

        try:
            response_json = response.json()
            status = extract_json_path(response_json, "$.data.status")
            assert status == "normal", f"期望状态 'normal'，实际状态 '{status}': {response.text[:200]}"
        except Exception as e:
            assert False, f"解析响应或检查状态失败: {e}"