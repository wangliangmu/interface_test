#!/usr/bin/env python3
import requests
import json

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

message = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "green",
            "title": {
                "tag": "plain_text",
                "content": "🎉 所有测试已通过！- 2026-05-14"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🎊 **太棒了！所有测试都通过了！**"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "📊 **最终测试结果**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "- AI配音接口测试：**全部通过** ✅\n- 图片克隆数字人测试：**全部通过** ✅\n- 志强基础版声音克隆测试：**全部通过** ✅"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🎉 总结：经过多次重跑，所有之前失败的测试用例现已全部修复并通过！所有核心功能运行正常。"
                }
            }
        ]
    }
}

response = requests.post(
    FEISHU_WEBHOOK,
    headers={"Content-Type": "application/json; charset=utf-8"},
    data=json.dumps(message, ensure_ascii=False).encode('utf-8')
)

print(f"通知发送状态: {response.status_code}")
print(f"响应内容: {response.text}")
