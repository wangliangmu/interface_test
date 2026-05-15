#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import pytz

# 飞书 Webhook 地址
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

def get_beijing_now():
    """获取当前北京时间的 datetime 对象"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)

# 获取当前日期（北京时间）
current_date = get_beijing_now().strftime("%Y-%m-%d")

# 测试报告数据
test_data = {
    "execution_time": current_date,
    "total_tests": 99,
    "passed": 96,
    "failed": 3,
    "skipped": 0,
    "failed_cases": [
        {
            "name": "test_ai配音接口测试.py::TestAi配音接口测试::test_step_05_post_voice_audition",
            "error_type": "功能问题",
            "reason": "期望音频内容大于 44 字节，实际为 0 字节",
            "suggestion": "检查 AI 配音服务是否正常工作，确认音频生成接口的响应内容"
        },
        {
            "name": "test_图片克隆数字人.py::Test图片克隆数字人::test_step_06_post_human_get",
            "error_type": "功能问题",
            "reason": "期望状态为 \"normal\"，实际为 \"failed\"，失败原因：上传文件失败",
            "suggestion": "检查图片克隆服务的文件上传功能是否正常"
        },
        {
            "name": "test_志强基础版声音克隆.py::Test志强基础版声音克隆::test_step_04_post_voiceclone_get",
            "error_type": "功能问题",
            "reason": "期望状态为 \"normal\"，实际为 \"failed\"，失败原因：声音克隆失败",
            "suggestion": "检查声音克隆服务的处理流程是否正常"
        }
    ]
}

# 构建飞书卡片消息
card_message = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red" if test_data["failed"] > 0 else "green",
            "title": {
                "tag": "plain_text",
                "content": f"每日接口测试报告 - {current_date}"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📊 测试执行摘要**\n- 执行时间：{test_data['execution_time']}\n- 总用例数：{test_data['total_tests']}\n- ✅ 通过：{test_data['passed']}\n- ❌ 失败：{test_data['failed']}\n- ⏭️ 跳过：{test_data['skipped']}"
                }
            },
            {
                "tag": "hr"
            }
        ]
    }
}

# 如果有失败的测试用例，添加详细信息
if test_data["failed"] > 0:
    card_message["card"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "**❌ 失败用例分析：**"
        }
    })
    
    for i, case in enumerate(test_data["failed_cases"], 1):
        card_message["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{i}. {case['name']}**\n- 错误类型：{case['error_type']}\n- 原因：{case['reason']}\n- 建议：{case['suggestion']}"
            }
        })
        # 添加分隔符
        if i < len(test_data["failed_cases"]):
            card_message["card"]["elements"].append({"tag": "hr"})

# 添加结论部分
conclusion = "整体测试结果：有 {} 个用例失败，请相关同事尽快排查问题。".format(test_data["failed"]) if test_data["failed"] > 0 else "✅ 所有测试用例均通过！"
card_message["card"]["elements"].extend([
    {
        "tag": "hr"
    },
    {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**✅ 结论：** {conclusion}"
        }
    }
])

# 发送请求
def send_notification():
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers={"Content-Type": "application/json; charset=utf-8"},
            data=json.dumps(card_message)
        )
        response.raise_for_status()
        print("飞书通知发送成功！")
        print(response.json())
    except Exception as e:
        print(f"发送飞书通知失败：{e}")

if __name__ == "__main__":
    send_notification()
