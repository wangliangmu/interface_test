#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import pytz

def get_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def main():
    # Test results
    summary = {
        "passed": 91,
        "failed": 2,
        "skipped": 6,
        "total": 99,
        "status": "失败",
        "execution_time": "2026-06-01 07:40:39 (耗时 1439.31秒)"
    }

    # Build Feishu card
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

    card_content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": "red",
                "title": {
                    "content": f"每日接口测试报告 - {datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')}",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": f"📊 测试执行摘要\n- 执行时间：{summary['execution_time']}\n- 测试结果：{summary['status']}\n- 共执行：{summary['total']} 个\n- 通过：{summary['passed']} 个\n- 失败：{summary['failed']} 个\n- 跳过：{summary['skipped']} 个",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "❌ 失败用例分析：\n1. tests/test_图片克隆数字人.py::Test图片克隆数字人::test_step_06_post_human_get\n   - 错误类型：功能问题\n   - 原因：合成照片视频失败，状态为failed\n   - 建议：检查图片克隆相关功能\n\n2. tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_04_post_video_get\n   - 错误类型：功能问题\n   - 原因：视频合成长时间处于producing状态未完成\n   - 建议：检查视频合成任务处理逻辑或增加等待时间",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "✅ 结论：存在失败测试用例，需要排查相关功能问题",
                        "tag": "lark_md"
                    }
                }
            ]
        }
    }

    # Send request
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(webhook_url, json=card_content, headers=headers)
        response.raise_for_status()
        print("Notification sent successfully!")
        print(response.text)
    except Exception as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    main()