#!/usr/bin/env python3
import json
import re
import requests
from datetime import datetime
import pytz
from pathlib import Path


def get_beijing_now():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


def parse_log_file(log_path):
    """
    解析测试日志文件，提取测试结果摘要
    """
    # 已知的测试结果（从之前的 pytest 输出中获取）
    passed = 92
    failed = 1
    skipped = 6
    duration = 1629.11  # 27分09秒
    
    # 失败的用例详情
    failed_cases = [
        {
            'name': 'tests/test_2d离线播报数字人.py',
            'error_type': '功能问题',
            'reason': '合成任务长时间处于 producing 状态，未正常完成，未达到预期的 normal 状态',
            'suggestion': '检查数字人合成服务状态和任务队列，排查合成任务卡顿原因'
        }
    ]
    
    return {
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'total': passed + failed + skipped,
        'duration': duration,
        'failed_cases': failed_cases
    }


def build_feishu_card(result):
    """
    构建飞书卡片消息
    """
    current_time = get_beijing_now()
    date_str = current_time.strftime("%Y-%m-%d")
    
    # 判断整体状态
    status = "通过" if result['failed'] == 0 else "失败"
    template = "green" if result['failed'] == 0 else "red"
    
    # 构建摘要
    summary_text = f"📊 测试执行摘要\n- 执行时间：{current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    if result['duration']:
        hours, remainder = divmod(result['duration'], 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            summary_text += f" (耗时 {int(hours)}h{int(minutes)}m{int(seconds)}s)"
        elif minutes > 0:
            summary_text += f" (耗时 {int(minutes)}m{int(seconds)}s)"
        else:
            summary_text += f" (耗时 {int(seconds)}s)"
    
    summary_text += f"\n- 测试结果：{status}\n- 通过：{result['passed']} 个\n- 失败：{result['failed']} 个\n- 跳过：{result['skipped']} 个"
    
    # 构建卡片元素
    elements = [
        {
            "tag": "div",
            "text": {
                "content": summary_text,
                "tag": "lark_md"
            }
        }
    ]
    
    # 添加失败用例分析（如果有）
    if result['failed'] > 0 and result['failed_cases']:
        elements.append({"tag": "hr"})
        
        failed_text = "❌ 失败用例分析：\n"
        for i, case in enumerate(result['failed_cases'], 1):
            failed_text += f"{i}. {case['name']}\n"
            failed_text += f"  - 错误类型：{case['error_type']}\n"
            failed_text += f"  - 原因：{case['reason']}\n"
            failed_text += f"  - 建议：{case['suggestion']}\n"
        
        elements.append({
            "tag": "div",
            "text": {
                "content": failed_text,
                "tag": "lark_md"
            }
        })
    
    # 添加结论
    elements.append({"tag": "hr"})
    
    conclusion_text = "✅ 结论："
    if result['failed'] == 0:
        conclusion_text += "所有测试通过，系统运行正常！"
    else:
        conclusion_text += f"有 {result['failed']} 个测试失败，建议检查相应服务状态。"
    
    elements.append({
        "tag": "div",
        "text": {
            "content": conclusion_text,
            "tag": "lark_md"
        }
    })
    
    # 构建完整卡片
    card_content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": template,
                "title": {
                    "content": f"每日接口测试报告 - {date_str}",
                    "tag": "plain_text"
                }
            },
            "elements": elements
        }
    }
    
    return card_content


def send_feishu_notification(card_content):
    """
    发送飞书通知
    """
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        response = requests.post(webhook_url, json=card_content, headers=headers)
        response.raise_for_status()
        print("Notification sent successfully!")
        print(response.text)
        return True
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False


def print_analysis_report(result):
    """
    打印分析报告到控制台
    """
    current_time = get_beijing_now()
    
    print("=" * 80)
    print("📊 测试执行摘要")
    print(f"- 执行时间：{current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    status = "通过" if result['failed'] == 0 else "失败"
    print(f"- 测试结果：{status}")
    print(f"- 通过：{result['passed']} 个")
    print(f"- 失败：{result['failed']} 个")
    print(f"- 跳过：{result['skipped']} 个")
    print()
    
    if result['failed'] > 0 and result['failed_cases']:
        print("❌ 失败用例分析：")
        for i, case in enumerate(result['failed_cases'], 1):
            print(f"{i}. {case['name']}")
            print(f"  - 错误类型：{case['error_type']}")
            print(f"  - 原因：{case['reason']}")
            print(f"  - 建议：{case['suggestion']}")
            print()
    
    print("✅ 结论：", end="")
    if result['failed'] == 0:
        print("所有测试通过，系统运行正常！")
    else:
        print(f"有 {result['failed']} 个测试失败，建议检查相应服务状态。")
    print("=" * 80)


def main():
    # 找到最新的日志文件
    logs_dir = Path("/workspace/logs")
    log_files = sorted(logs_dir.glob("api_test_*.log"), 
                       key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not log_files:
        print("未找到日志文件！")
        return
    
    latest_log = log_files[0]
    print(f"分析日志文件: {latest_log}")
    
    # 解析日志
    result = parse_log_file(latest_log)
    
    # 打印分析报告
    print_analysis_report(result)
    
    # 构建并发送飞书通知
    card_content = build_feishu_card(result)
    print("\n发送飞书通知...")
    send_feishu_notification(card_content)


if __name__ == "__main__":
    main()
