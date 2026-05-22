#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# 飞书 Webhook 地址
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

# 测试结果数据
EXECUTION_TIME = "2026-05-22 00:41:57"
TOTAL_TESTS = 99
PASSED_TESTS = 97
FAILED_TESTS = 2
SKIPPED_TESTS = 0
PASS_RATE = "98.0%"

# 失败用例分析
FAILED_CASES = [
    {
        "name": "test_step_04_post_human_get",
        "class": "Test2d换脸克隆",
        "file": "test_2d换脸克隆.py",
        "error_type": "功能问题",
        "reason": "2D换脸任务异步处理失败，状态为'failed'，失败原因: '视频换脸失败'",
        "suggestion": "检查换脸服务是否正常工作，检查输入的人脸照片和目标视频是否符合要求"
    },
    {
        "name": "test_step_04_post_voiceclone_get",
        "class": "Test志强基础版声音克隆",
        "file": "test_志强基础版声音克隆.py",
        "error_type": "功能问题",
        "reason": "声音克隆任务异步处理失败，状态为'failed'",
        "suggestion": "检查声音克隆服务是否正常工作，检查输入的音频文件是否符合要求"
    }
]

# 构建飞书卡片消息
def build_feishu_card():
    is_success = FAILED_TESTS == 0
    header_color = "green" if is_success else "red"
    title = f"每日接口测试报告 - {EXECUTION_TIME.split()[0]}"
    
    # 测试摘要部分
    summary_content = [
        f"📊 测试执行摘要",
        f"- 执行时间: {EXECUTION_TIME}",
        f"- 测试结果: {'通过' if is_success else '失败'}",
        f"- 通过: {PASSED_TESTS} 个",
        f"- 失败: {FAILED_TESTS} 个",
        f"- 跳过: {SKIPPED_TESTS} 个",
        f"- 通过率: {PASS_RATE}"
    ]
    
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(summary_content)
            }
        }
    ]
    
    # 如果有失败用例，添加失败用例分析
    if not is_success:
        elements.append({"tag": "hr"})
        
        failed_content = ["❌ 失败用例分析:"]
        for i, case in enumerate(FAILED_CASES, 1):
            failed_content.append(f"{i}. {case['class']}::{case['name']}")
            failed_content.append(f"   - 错误类型: {case['error_type']}")
            failed_content.append(f"   - 原因: {case['reason']}")
            failed_content.append(f"   - 建议: {case['suggestion']}")
        
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(failed_content)
            }
        })
    
    # 添加结论
    elements.append({"tag": "hr"})
    conclusion = "✅ 结论: 大部分接口测试通过，仅有2个异步处理任务失败，建议重点排查2D换脸和声音克隆服务。" if not is_success else "✅ 结论: 所有测试通过！"
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": conclusion
        }
    })
    
    # 构建完整消息
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": header_color,
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": elements
        }
    }
    
    return message

# 发送飞书通知
def send_feishu_notification():
    message = build_feishu_card()
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(message),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10
        )
        
        result = response.json()
        if result.get("code") == 0:
            print("飞书通知发送成功！")
        else:
            print(f"飞书通知发送失败: {result}")
            
    except Exception as e:
        print(f"发送飞书通知时发生错误: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("📊 测试执行摘要")
    print(f"- 执行时间: {EXECUTION_TIME}")
    print(f"- 测试结果: {'通过' if FAILED_TESTS == 0 else '失败'}")
    print(f"- 通过: {PASSED_TESTS} 个")
    print(f"- 失败: {FAILED_TESTS} 个")
    print(f"- 跳过: {SKIPPED_TESTS} 个")
    print(f"- 通过率: {PASS_RATE}")
    print("=" * 60)
    print("\n❌ 失败用例分析:")
    
    for i, case in enumerate(FAILED_CASES, 1):
        print(f"{i}. {case['class']}::{case['name']}")
        print(f"   - 错误类型: {case['error_type']}")
        print(f"   - 原因: {case['reason']}")
        print(f"   - 建议: {case['suggestion']}")
        print()
    
    print("=" * 60)
    conclusion = "✅ 结论: 大部分接口测试通过，仅有2个异步处理任务失败，建议重点排查2D换脸和声音克隆服务。" if FAILED_TESTS > 0 else "✅ 结论: 所有测试通过！"
    print(conclusion)
    print("=" * 60)
    
    print("\n正在发送飞书通知...")
    send_feishu_notification()
