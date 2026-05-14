#!/usr/bin/env python3
import requests
import json

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# 构建飞书卡片消息
message = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "失败测试重跑结果 - 2026-05-14"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "📊 **重跑结果汇总"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "- 重跑用例数: **3个**\n- 修复成功: **1个**\n- 仍然失败: **2个**"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "✅ **修复成功**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "- **图片克隆数字人测试** - **全部通过**"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "❌ **仍然失败**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "- **AI配音接口测试** - 第5步失败：预期音频内容 &gt; 44字节，但实际返回 0 字节\n- **志强基础版声音克隆测试** - 状态仍为 failed"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🎉 总结：图片克隆问题已解决，AI配音和声音克隆需要进一步排查。"
                }
            }
        ]
    }
}

# 发送请求
response = requests.post(
    FEISHU_WEBHOOK,
    headers={"Content-Type": "application/json; charset=utf-8"},
    data=json.dumps(message, ensure_ascii=False).encode('utf-8')
)

print(f"通知发送状态: {response.status_code}")
print(f"响应内容: {response.text}")
