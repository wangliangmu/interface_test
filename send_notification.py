#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import pytz

# Get current Beijing time
def get_beijing_now():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# Test data
passed_count = 98
failed_count = 1
skipped_count = 0
execution_time = "2026-05-20 23:42:25"
is_success = failed_count == 0

# Prepare card
card = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green" if is_success else "red",
            "title": {
                "tag": "plain_text",
                "content": f"每日接口测试报告 - {get_beijing_now().strftime('%Y-%m-%d')}"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"📊 **测试执行摘要**\n- 执行时间: {execution_time}\n- 测试结果: {'通过 ✅' if is_success else '失败 ❌'}\n- 通过: {passed_count} 个\n- 失败: {failed_count} 个\n- 跳过: {skipped_count} 个"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "❌ **失败用例分析**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "1. **tests/test_创建网页类型对话.py::Test创建网页类型对话::test_step_05_post_dialogs_get**\n- 错误类型: 功能问题\n- 原因: 期望状态 'success'，实际状态 'failed'\n- 建议: 检查接口功能是否正常"
                }
            }
        ]
    }
}

# Send
response = requests.post(
    webhook_url,
    headers={"Content-Type": "application/json; charset=utf-8"},
    data=json.dumps(card, ensure_ascii=False)
)
print(f"Notification sent: {response.status_code} - {response.text}")

# Print summary
print("\n📊 测试执行摘要")
print(f"- 执行时间: {execution_time}")
print(f"- 测试结果: {'通过' if is_success else '失败'}")
print(f"- 通过: {passed_count} 个")
print(f"- 失败: {failed_count} 个")
print(f"- 跳过: {skipped_count} 个")

print("\n❌ 失败用例分析:")
print("1. tests/test_创建网页类型对话.py::Test创建网页类型对话::test_step_05_post_dialogs_get")
print("   - 错误类型: 功能问题")
print("   - 原因: 期望状态 'success'，实际状态 'failed'")
print("   - 建议: 检查接口功能是否正常")

print("\n✅ 结论: 存在失败用例，请根据分析进行排查")
