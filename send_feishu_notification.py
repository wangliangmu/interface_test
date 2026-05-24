#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def send_feishu_notification():
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    
    execution_date = datetime.now().strftime("%Y-%m-%d")
    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    template_color = "red"  # 失败用红色
    passed = 86
    failed = 5
    skipped = 8
    
    if failed == 0:
        template_color = "green"
    
    # 构建卡片内容
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": template_color,
                "title": {
                    "content": f"每日接口测试报告 - {execution_date}",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": f"📊 测试执行摘要\n- 执行时间: {execution_time}\n- 通过: {passed} 个\n- 失败: {failed} 个\n- 跳过: {skipped} 个",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "❌ 失败用例分析:",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "1. test_ai配音接口测试\n   - 错误类型: 功能问题\n   - 原因: 测试期望返回 Content-Type 为 audio/wav，但实际返回了 application/json\n   - 建议: 检查 AI 配音服务接口是否正常工作，或更新测试用例的断言逻辑",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "2. test_ai职业照接口测试\n   - 错误类型: 环境问题\n   - 原因: 接口返回了 504 Gateway Time-out 错误，表示请求超时\n   - 建议: 检查 AI 职业照服务的可用性和性能，增加超时时间或优化服务端",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "3. test_创建网页类型对话\n   - 错误类型: 功能问题\n   - 原因: 对话状态期望为 'success'，但实际状态为 'failed'\n   - 建议: 检查网页类型对话创建流程，排查失败原因",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "4. test_2d离线播报数字人\n   - 错误类型: 功能问题\n   - 原因: 期望状态为 'normal'，实际状态为 'failed'，错误信息为 'tts生成失败'\n   - 建议: 检查 2D 离线播报数字人服务，特别是 TTS 生成相关组件",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "5. test_志强基础版声音克隆\n   - 错误类型: 功能问题\n   - 原因: 期望状态为 'normal'，实际状态为 'failed'，错误信息为 '声音克隆失败'\n   - 建议: 检查志强基础版声音克隆服务，排查克隆失败原因",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": f"✅ 结论: 总共有 {passed} 个测试用例通过，{failed} 个失败，请重点关注上述失败用例的修复。",
                        "tag": "lark_md"
                    }
                }
            ]
        }
    }
    
    # 发送请求
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(card))
    
    print(f"发送状态: {response.status_code}")
    print(f"响应内容: {response.text}")

if __name__ == "__main__":
    send_feishu_notification()
