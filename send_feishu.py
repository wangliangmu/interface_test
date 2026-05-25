import requests
import json
from datetime import datetime

# 飞书 Webhook 地址
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# 测试执行摘要
total_passed = 90
total_failed = 3
total_skipped = 6

# 失败用例详情
failed_cases = [
    {
        "name": "Test2d离线播报数字人::test_step_04_post_video_get",
        "error_type": "功能问题",
        "reason": "期望状态 'normal'，实际状态 'producing'",
        "suggestion": "检查2D离线播报任务可能存在异常，建议检查任务执行逻辑或相关服务状态"
    },
    {
        "name": "Test志强基础版声音克隆::test_step_04_post_voiceclone_get",
        "error_type": "功能问题",
        "reason": "期望状态 'normal'，实际状态 'failed'",
        "suggestion": "声音克隆任务失败，建议检查声音克隆服务状态和相关日志"
    },
    {
        "name": "Test精品克隆音频检测接口测试::test_step_02_post_voiceclone_checkwer",
        "error_type": "测试数据问题",
        "reason": "期望结果 '音频识别合格'，实际结果 '音频识别较差，建议重新录制'",
        "suggestion": "音频检测接口返回检测结果不符合预期，建议检查测试音频质量或调整检测阈值"
    }
]

# 构建飞书卡片消息
date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 判断测试结果状态
header_template = "red" if total_failed > 0 else "green"
result_text = "有失败用例" if total_failed > 0 else "全部通过"

# 构建卡片内容
card_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": header_template,
            "title": {
                "content": f"每日接口测试报告 - {date_str}",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "📊 **测试执行摘要",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "text": {
                    "content": f"- **执行时间**: {date_str}\n- **测试结果**: {result_text}\n- **通过**: {total_passed} 个\n- **失败**: {total_failed} 个\n- **跳过**: {total_skipped} 个",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "content": "❌ **失败用例分析**:",
                    "tag": "lark_md"
                }
            }
        ]
    }
}

# 添加失败用例详情
for i, case in enumerate(failed_cases, 1):
    card_content["card"]["elements"].append({
        "tag": "div",
        "text": {
            "content": f"**{i}. {case['name']}**\n- **错误类型**: {case['error_type']}\n- **原因**: {case['reason']}\n- **建议**: {case['suggestion']}",
            "tag": "lark_md"
        }
    })

# 添加结论
conclusion = "有部分测试用例失败，请开发人员关注并及时修复相关问题" if total_failed > 0 else "所有测试用例均通过，接口运行正常"

card_content["card"]["elements"].append({
    "tag": "hr"
})

card_content["card"]["elements"].append({
    "tag": "div",
    "text": {
        "content": f"✅ **结论**: {conclusion}",
        "tag": "lark_md"
    }
})

# 发送飞书通知
headers = {
    "Content-Type": "application/json; charset=utf-8"
}

response = requests.post(webhook_url, headers=headers, json=card_content)

print("飞书通知发送状态码:", response.status_code)
print("响应内容:", response.text)

# 打印测试报告到控制台
print("\n" + "=" * 80)
print("📊 测试执行摘要")
print("=" * 80)
print(f"- 执行时间: {date_str}")
print(f"- 测试结果: {result_text}")
print(f"- 通过: {total_passed} 个")
print(f"- 失败: {total_failed} 个")
print(f"- 跳过: {total_skipped} 个")
print("\n❌ 失败用例分析:")
for i, case in enumerate(failed_cases, 1):
    print(f"\n{i}. {case['name']}")
    print(f"   - 错误类型: {case['error_type']}")
    print(f"   - 原因: {case['reason']}")
    print(f"   - 建议: {case['suggestion']}")
print("\n" + "=" * 80)
print(f"✅ 结论: {conclusion}")
print("=" * 80)
