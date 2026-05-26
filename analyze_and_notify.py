#!/usr/bin/env python3
import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path
import pytz


def get_beijing_now():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


def parse_test_summary(log_path):
    summary = {"passed": 0, "failed": 0, "skipped": 0, "total": 0}
    failures = []

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse short test summary: e.g. "2 failed, 91 passed, 6 skipped in 927.21s"
    match = re.search(r"(\d+) failed, (\d+) passed, (\d+) skipped", content)
    if match:
        summary["failed"] = int(match.group(1))
        summary["passed"] = int(match.group(2))
        summary["skipped"] = int(match.group(3))
        summary["total"] = summary["failed"] + summary["passed"] + summary["skipped"]

    # Parse failures
    # FAILED tests/test_xxx.py::TestClass::test_method - AssertionError: ...
    failure_blocks = re.findall(r"FAILED (.*?) - (AssertionError:.*?)(?=\n\S|$)", content, re.DOTALL)
    for test_name, error in failure_blocks:
        test_name = test_name.strip()
        error = error.strip()
        # Determine error type
        error_type = "功能问题"
        if "timeout" in error.lower() or "连接失败" in error or "服务不可用" in error:
            error_type = "环境问题"
        elif "认证失败" in error or "token过期" in error:
            error_type = "权限问题"
        elif "测试依赖的数据不存在" in error or "格式错误" in error:
            error_type = "测试数据问题"
        failures.append({"name": test_name, "error": error, "type": error_type})

    return summary, failures


def send_feishu_notification(summary, failures, webhook_url):
    date_str = get_beijing_now().strftime("%Y-%m-%d")
    overall_result = "失败" if summary["failed"] > 0 else "通过"
    template = "red" if summary["failed"] > 0 else "green"

    elements = [
        {
            "tag": "markdown",
            "content": f"📊 **测试执行摘要**\n- 执行时间: {get_beijing_now().strftime('%Y-%m-%d %H:%M:%S')}\n- 测试结果: {overall_result}\n- 通过: {summary['passed']} 个\n- 失败: {summary['failed']} 个\n- 跳过: {summary['skipped']} 个"
        }
    ]

    if failures:
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": "❌ **失败用例分析**"})
        for i, failure in enumerate(failures, 1):
            elements.append({
                "tag": "markdown",
                "content": f"{i}. {failure['name']}\n   - 错误类型: {failure['type']}\n   - 原因: {failure['error'][:300]}\n   - 建议: 请检查相关功能"
            })

    elements.append({"tag": "hr"})
    conclusion = "测试通过，所有功能正常运行！" if summary["failed"] == 0 else "测试存在失败，请相关人员检查修复！"
    elements.append({"tag": "markdown", "content": f"✅ **结论**: {conclusion}"})

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": template,
                "title": {
                    "content": f"每日接口测试报告 - {date_str}",
                    "tag": "plain_text"
                }
            },
            "elements": elements
        }
    }

    response = requests.post(webhook_url, json=payload)
    print(f"Feishu notification response: {response.status_code}, {response.text}")
    return response


def main():
    # Use the test results we got from the run
    summary = {"passed": 91, "failed": 2, "skipped": 6, "total": 99}
    failures = [
        {
            "name": "tests/test_创建网页类型对话_带动作.py::Test创建网页类型对话带动作::test_step_05_post_dialogs_get",
            "error": "AssertionError: 解析响应或检查状态失败: 期望状态 'success'，实际状态 'failed'",
            "type": "功能问题"
        },
        {
            "name": "tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_04_post_video_get",
            "error": "AssertionError: 解析响应或检查状态失败: 期望状态 'normal'，实际状态 'failed', fail_reason: '合成动作背景视频失败'",
            "type": "功能问题"
        }
    ]
    print(f"Test summary: {summary}")
    print(f"Failures: {failures}")

    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    send_feishu_notification(summary, failures, webhook_url)


if __name__ == "__main__":
    main()
