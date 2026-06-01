#!/usr/bin/env python3
"""
分析测试结果并发送飞书通知
"""
import json
import os
from datetime import datetime
import pytz
import glob
import requests


def get_latest_file(pattern):
    """获取最新的文件"""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)


def analyze_test_results():
    """分析测试结果"""
    result = {
        "execution_time": "2026-06-02 07:42:22",
        "status": "failure",
        "passed": 88,
        "failed": 5,
        "skipped": 6,
        "failures": [
            {
                "name": "test_ai职业照接口测试",
                "error_type": "功能问题",
                "reason": "期望状态 'success'，实际状态 'producing'",
                "suggestion": "检查AI职业照合成任务是否超时或处理异常"
            },
            {
                "name": "test_图片克隆数字人",
                "error_type": "功能问题",
                "reason": "期望状态 'normal'，实际状态 'failed'，失败原因：合成alpha视频失败",
                "suggestion": "检查图片克隆合成服务是否正常工作"
            },
            {
                "name": "test_ai卡通照片接口测试",
                "error_type": "功能问题",
                "reason": "期望状态 'success'，实际状态 'failed'",
                "suggestion": "检查AI卡通照片合成任务是否正常工作"
            },
            {
                "name": "test_2d离线播报数字人",
                "error_type": "功能问题",
                "reason": "期望状态 'normal'，实际状态 'producing'",
                "suggestion": "检查2D离线播报合成任务是否超时"
            },
            {
                "name": "test_2d视频克隆数字人",
                "error_type": "功能问题",
                "reason": "期望状态 'normal'，实际状态 'failed'，失败原因：合成alpha视频失败",
                "suggestion": "检查2D视频克隆合成服务是否正常工作"
            }
        ]
    }
    return result


def send_feishu_notification(result):
    """发送飞书通知"""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    
    # 构建消息内容
    title = f"每日接口测试报告 - 2026-06-02"
    
    summary_text = f"📊 测试执行摘要\n- 执行时间: {result['execution_time']}\n- 测试结果: 失败 ✗\n- 通过: {result['passed']} 个\n- 失败: {result['failed']} 个\n- 跳过: {result['skipped']} 个"
    
    failure_text = "❌ 失败用例分析:\n"
    for i, failure in enumerate(result['failures'], 1):
        failure_text += f"{i}. {failure['name']}\n"
        failure_text += f"   - 错误类型: {failure['error_type']}\n"
        failure_text += f"   - 原因: {failure['reason']}\n"
        failure_text += f"   - 建议: {failure['suggestion']}\n\n"
    
    conclusion_text = "✅ 结论: 部分接口测试失败，主要涉及数字人合成相关功能，请相关人员及时排查问题"
    
    # 构建飞书卡片消息
    card_content = {
        "header": {
            "template": "red",
            "title": {
                "tag": "plain_text",
                "content": title
            }
        },
        "elements": [
            {
                "tag": "markdown",
                "content": summary_text
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": failure_text
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "markdown",
                "content": conclusion_text
            }
        ]
    }
    
    message = {
        "msg_type": "interactive",
        "card": card_content
    }
    
    # 发送请求
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print("飞书通知发送成功")
        return True
    except Exception as e:
        print(f"飞书通知发送失败: {e}")
        return False


if __name__ == "__main__":
    print("开始分析测试结果...")
    test_result = analyze_test_results()
    
    print("测试结果:")
    print(f"  通过: {test_result['passed']}")
    print(f"  失败: {test_result['failed']}")
    print(f"  跳过: {test_result['skipped']}")
    
    print("\n发送飞书通知...")
    send_feishu_notification(test_result)
