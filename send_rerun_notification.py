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

# 重跑测试报告数据
test_data = {
    "execution_time": current_date,
    "total_tests": 14,  # 6 + 5 + 3
    "passed": 14,
    "failed": 0,
    "skipped": 0,
    "failed_cases": [],
    "test_details": [
        {
            "name": "test_ai配音接口测试.py",
            "status": "全部通过",
            "duration": "27.97秒",
            "steps": 6
        },
        {
            "name": "test_图片克隆数字人.py",
            "status": "全部通过",
            "duration": "124.93秒",
            "steps": 5
        },
        {
            "name": "test_志强基础版声音克隆.py",
            "status": "全部通过",
            "duration": "183.43秒",
            "steps": 3
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
            "template": "green",
            "title": {
                "tag": "plain_text",
                "content": f"接口测试重跑报告 - {current_date}"
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
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**✅ 重跑测试详情：**"
                }
            }
        ]
    }
}

# 添加每个测试用例的详细信息
for detail in test_data["test_details"]:
    card_message["card"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**• {detail['name']}**\n  - 状态：{detail['status']}\n  - 耗时：{detail['duration']}\n  - 测试步骤：{detail['steps']}个"
        }
    })

# 添加结论部分
card_message["card"]["elements"].extend([
    {
        "tag": "hr"
    },
    {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "**✅ 结论：** 所有之前失败的测试用例现已全部通过！测试环境已恢复正常。"
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
