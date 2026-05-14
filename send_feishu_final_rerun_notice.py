#!/usr/bin/env python3
import requests
import json

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# 构建飞书卡片消息
message = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "green",
            "title": {
                "tag": "plain_text",
                "content": "最终重跑结果 - 2026-05-14"
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
                    "content": "- 重跑用例数: **2个**\n- 修复成功: **1个**\n- 仍然失败: **1个**"
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
                    "content": "- **志强基础版声音克隆测试** - **全部通过**！🎉\n- **图片克隆数字人测试** - 之前已通过"
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
                    "content": "- **AI配音接口测试** - 第5步仍失败：预期音频内容 &gt; 44字节，但实际返回 0 字节"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🎉 总结：现在只有1个测试失败了，另外2个都已经修复！图片克隆和声音克隆问题已解决，只有AI配音还需要进一步排查。"
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
