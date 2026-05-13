#!/usr/bin/env python3
import requests
import json

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# 构建飞书卡片消息
message = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "red",
            "title": {
                "tag": "plain_text",
                "content": "每日接口测试报告 - 2026-05-13"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "📊 **测试执行摘要**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "- 测试结果：**失败**\n- 通过：**95** 个\n- 失败：**3** 个\n- 跳过：**0** 个"
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
                    "content": "**1. AI配音接口测试**\n- 错误类型：功能问题\n- 原因：预期音频内容 > 44字节，但实际返回 0 字节\n- 建议：检查音频生成接口的实现逻辑"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**2. 图片克隆数字人测试**\n- 错误类型：功能问题\n- 原因：期望状态 'normal'，实际状态 'failed'，错误信息为\"合成照片视频失败\"\n- 建议：检查图片克隆功能的实现"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**3. 志强基础版声音克隆测试**\n- 错误类型：功能问题\n- 原因：期望状态 'normal'，实际状态 'failed'，错误信息为\"声音克隆失败\"\n- 建议：检查声音克隆功能的实现"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "✅ **结论**：整体测试环境运行正常，但有3个核心功能测试失败，需要开发团队关注修复。"
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
