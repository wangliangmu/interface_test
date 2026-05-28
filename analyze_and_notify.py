#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import pytz
import os
import re


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
        "execution_time": "2026-05-29 07:40:59 (耗时 1437.92秒)"
    }

    failed_cases = [
        {
            "name": "tests/test_图片克隆数字人.py::Test图片克隆数字人::test_step_06_post_human_get",
            "error_type": "功能问题",
            "reason": "期望状态 'normal'，实际状态 'failed'",
            "suggestion": "检查图片克隆接口功能"
        },
        {
            "name": "tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_04_post_video_get",
            "error_type": "功能问题",
            "reason": "期望状态 'normal'，实际状态 'producing'",
            "suggestion": "检查2D离线播报接口功能或增加等待时间"
        }
    ]

    # Build Feishu card
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

    # Build report text
    report_text = f"""📊 测试执行摘要
- 执行时间：{summary['execution_time']}
- 测试结果：{summary['status']}
- 通过：{summary['passed']} 个
- 失败：{summary['failed']} 个
- 跳过：{summary['skipped']} 个

❌ 失败用例分析：
"""

    for i, case in enumerate(failed_cases, 1):
        report_text += f"{i}. {case['name']}\n"
        report_text += f"   - 错误类型：{case['error_type']}\n"
        report_text += f"   - 原因：{case['reason']}\n"
        report_text += f"   - 建议：{case['suggestion']}\n"
        report_text += "\n"

    report_text += "✅ 结论：存在失败测试用例，请检查相关接口功能。"

    card_content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": "red" if summary["failed"] > 0 else "green",
                "title": {
                    "content": f"每日接口测试报告 - {datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')}",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": report_text,
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
        print("Response:", response.text)
    except Exception as e:
        print(f"Failed to send notification: {e}")


if __name__ == "__main__":
    main()
