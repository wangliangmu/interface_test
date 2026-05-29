#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import pytz

def get_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def main():
    # Test results (skip_in_full_run 标记的用例不计入统计)
    summary = {
        "passed": 92,
        "failed": 1,
        "skipped": 6,
        "total": 99,
        "status": "失败",
        "execution_time": "2026-05-30 07:17:11 (耗时 1417.28秒)"
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
                        "content": "❌ 失败用例分析：\n1. tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_04_post_video_get\n  - 错误类型：功能问题/超时\n  - 原因：期望状态 'normal'，实际状态一直为 'producing'，等待超时\n  - 建议：检查 2D 离线播报任务处理服务是否正常，或延长等待时间",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "✅ 结论：大部分测试通过，但有一个 2D 离线播报用例超时，需要关注！",
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