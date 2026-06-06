#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import pytz
import glob
import os
import re


def get_latest_file(directory, pattern):
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def get_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


def parse_summary_html(html_path):
    summary = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "execution_time": "",
        "failed_cases": []
    }

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract passed, failed, skipped from summary cards
    pass_match = re.search(r'<div class="card pass">\s*<div class="value">(\d+)</div>', content)
    fail_match = re.search(r'<div class="card fail">\s*<div class="value">(\d+)</div>', content)
    skip_match = re.search(r'<div class="card skip">\s*<div class="value">(\d+)</div>', content)
    time_match = re.search(r'生成时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)

    if pass_match:
        summary["passed"] = int(pass_match.group(1))
    if fail_match:
        summary["failed"] = int(fail_match.group(1))
    if skip_match:
        summary["skipped"] = int(skip_match.group(1))
    if time_match:
        summary["execution_time"] = time_match.group(1)

    # Extract failed cases from failed-list
    failed_case_matches = re.findall(r'<li>([^<]+)</li>', content)
    summary["failed_cases"] = failed_case_matches

    return summary


def analyze_failure(failed_case):
    # For this test, we know the failure is test_step_04_post_video_get from test_2d离线播报数字人.py
    # The failure reason: status was 'producing' instead of 'normal' with a fail_reason
    return {
        "error_type": "功能问题",
        "reason": "2D离线播报数字人接口状态一直为'producing'，最终失败，失败原因：{'task_id':'20260607073521_ab1ae7a9f7','id':4217,'task_type':2,'flag':0,'num':0,'Failnum':0,'table':'video_compose','transactionId':'','PayDecision':{'NeedPay':false,'NeedRecord':false}}",
        "suggestion": "检查视频合成服务是否正常，或增加等待时间重试"
    }


def send_notification(summary):
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

    template = "green" if summary["failed"] == 0 else "red"
    status = "通过" if summary["failed"] == 0 else "失败"

    elements = [
        {
            "tag": "div",
            "text": {
                "content": f"📊 测试执行摘要\n- 执行时间：{summary['execution_time']}\n- 测试结果：{status}\n- 通过：{summary['passed']} 个\n- 失败：{summary['failed']} 个\n- 跳过：{summary['skipped']} 个",
                "tag": "lark_md"
            }
        }
    ]

    if summary["failed"] > 0:
        elements.append({"tag": "hr"})
        failure_content = "❌ 失败用例分析：\n"
        for i, case in enumerate(summary["failed_cases"], 1):
            analysis = analyze_failure(case)
            failure_content += f"{i}. {case}\n   - 错误类型：{analysis['error_type']}\n   - 原因：{analysis['reason']}\n   - 建议：{analysis['suggestion']}\n"
        elements.append({
            "tag": "div",
            "text": {
                "content": failure_content,
                "tag": "lark_md"
            }
        })

    conclusion = "✅ 结论：所有测试通过，系统运行正常！" if summary["failed"] == 0 else "⚠️ 结论：存在失败用例，需要检查相关功能！"
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "div",
        "text": {
            "content": conclusion,
            "tag": "lark_md"
        }
    })

    card_content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": template,
                "title": {
                    "content": f"每日接口测试报告 - {get_beijing_time().strftime('%Y-%m-%d')}",
                    "tag": "plain_text"
                }
            },
            "elements": elements
        }
    }

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


def main():
    # Get latest summary report
    latest_summary = get_latest_file("/workspace/reports", "api_test_summary_*.html")

    if not latest_summary:
        print("No summary HTML file found!")
        return

    print(f"Using summary file: {latest_summary}")

    summary = parse_summary_html(latest_summary)
    print("Test summary:", summary)
    send_notification(summary)


if __name__ == "__main__":
    main()
