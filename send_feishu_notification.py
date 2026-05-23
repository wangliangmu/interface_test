
import requests
import json
from datetime import datetime

# Webhook URL
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# Test execution summary
execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
passed = 91
failed = 2
skipped = 6
test_result = "失败" if failed > 0 else "通过"

# Failed cases analysis
failed_cases = [
    {
        "name": "tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_04_post_video_get",
        "error_type": "功能问题",
        "reason": "接口返回状态为 'producing'，期望状态为 'normal'",
        "suggestion": "检查2D离线播报数字人任务生成逻辑，确认任务是否正常完成"
    },
    {
        "name": "tests/test_志强基础版声音克隆.py::Test志强基础版声音克隆::test_step_04_post_voiceclone_get",
        "error_type": "功能问题",
        "reason": "接口返回状态为 'failed'，期望状态为 'normal'，失败原因为 '声音克隆失败'",
        "suggestion": "检查志强基础版声音克隆功能，查看失败原因详情"
    }
]

# Build Feishu card message
card_content = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "red" if failed > 0 else "green",
            "title": {
                "content": f"每日接口测试报告 - {datetime.now().strftime('%Y-%m-%d')}",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📊 测试执行摘要**\n- 执行时间：{execution_time}\n- 测试结果：{test_result}\n- 通过：{passed} 个\n- 失败：{failed} 个\n- 跳过：{skipped} 个"
                }
            }
        ]
    }
}

# Add failed cases if any
if failed > 0:
    failed_text = "**❌ 失败用例分析**"
    for i, case in enumerate(failed_cases, 1):
        failed_text += f"\n{i}. {case['name']}\n   - 错误类型：{case['error_type']}\n   - 原因：{case['reason']}\n   - 建议：{case['suggestion']}"
    card_content["card"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": failed_text
        }
    })

# Add conclusion
conclusion = "**✅ 结论**：部分测试用例失败，请查看失败用例分析并修复相关问题" if failed > 0 else "**✅ 结论**：所有测试用例通过"
card_content["card"]["elements"].append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": conclusion
    }
})

# Send the request
response = requests.post(webhook_url, headers={"Content-Type": "application/json; charset=utf-8"}, data=json.dumps(card_content))
print("Feishu notification sent. Response:", response.status_code, response.text)

# Also print the analysis report in the required format
print("\n" + "="*50)
print("📊 测试执行摘要")
print(f"- 执行时间：{execution_time}")
print(f"- 测试结果：{test_result}")
print(f"- 通过：{passed} 个")
print(f"- 失败：{failed} 个")
print(f"- 跳过：{skipped} 个")
if failed > 0:
    print("\n❌ 失败用例分析：")
    for i, case in enumerate(failed_cases, 1):
        print(f"{i}. {case['name']}")
        print(f"   - 错误类型：{case['error_type']}")
        print(f"   - 原因：{case['reason']}")
        print(f"   - 建议：{case['suggestion']}")
print(f"\n✅ 结论：{conclusion}")
print("="*50)
