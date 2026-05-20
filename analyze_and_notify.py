#!/usr/bin/env python3
"""
分析测试结果并发送飞书通知
"""
import os
import re
import requests
import json
from datetime import datetime
from pathlib import Path
import pytz


def get_beijing_now():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


def main():
    project_root = Path(__file__).parent.absolute()
    logs_dir = project_root / "logs"
    reports_dir = project_root / "reports"

    # 获取最新的日志文件和报告
    log_files = sorted(logs_dir.glob("api_test_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    detail_html_files = sorted(reports_dir.glob("api_test_detail_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not log_files:
        print("未找到日志文件")
        return

    log_path = log_files[0]
    print(f"分析日志文件: {log_path}")

    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        log_content = f.read()

    # 提取执行摘要
    passed_count = 0
    failed_count = 0
    skipped_count = 0

    summary_match = re.search(r"(\d+) failed, (\d+) passed in", log_content)
    if summary_match:
        failed_count = int(summary_match.group(1))
        passed_count = int(summary_match.group(2))

    execution_time = get_beijing_now().strftime("%Y-%m-%d %H:%M:%S")

    # 分析失败用例
    failed_cases = []

    # 查找失败的测试
    # 从日志中查找 FAILED 后面的测试名称和错误信息
    test_name_pattern = re.compile(r"FAILED (tests/.*?::.*?::.*?) - ")
    error_pattern = re.compile(r"AssertionError: (.*?)\n")

    test_name_matches = test_name_pattern.findall(log_content)
    error_matches = error_pattern.findall(log_content)

    if test_name_matches:
        for i, test_name in enumerate(test_name_matches):
            error_msg = error_matches[i] if i < len(error_matches) else "未知错误"

            # 判断错误类型
            error_type = "功能问题"  # 默认
            if "timeout" in error_msg.lower() or "connection" in error_msg.lower() or "unavailable" in error_msg.lower():
                error_type = "环境问题"
            elif "token" in error_msg.lower() or "auth" in error_msg.lower() or "authentication" in error_msg.lower():
                error_type = "权限问题"
            elif "data" in error_msg.lower() or "not found" in error_msg.lower():
                error_type = "测试数据问题"

            failed_cases.append({
                "name": test_name,
                "type": error_type,
                "reason": error_msg,
                "suggestion": "检查接口功能是否正常"
            })

    # 准备飞书卡片
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    is_success = failed_count == 0

    card_template = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "green" if is_success else "red",
                "title": {
                    "tag": "plain_text",
                    "content": f"每日接口测试报告 - {get_beijing_now().strftime('%Y-%m-%d')}"
                }
            },
            "elements": []
        }
    }

    # 添加执行摘要
    summary_elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"📊 **测试执行摘要**\n- 执行时间: {execution_time}\n- 测试结果: {'通过 ✅' if is_success else '失败 ❌'}\n- 通过: {passed_count} 个\n- 失败: {failed_count} 个\n- 跳过: {skipped_count} 个"
            }
        }
    ]

    card_template["card"]["elements"].extend(summary_elements)

    # 添加失败用例分析（如果有）
    if failed_cases:
        card_template["card"]["elements"].append({
            "tag": "hr"
        })

        failed_elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "❌ **失败用例分析**"
                }
            }
        ]

        for i, case in enumerate(failed_cases, 1):
            failed_elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"{i}. **{case['name']}**\n- 错误类型: {case['type']}\n- 原因: {case['reason']}\n- 建议: {case['suggestion']}"
                }
            })

        card_template["card"]["elements"].extend(failed_elements)

    # 发送通知
    print("发送飞书通知...")
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps(card_template, ensure_ascii=False)
    )
    print(f"通知发送结果: {response.status_code} - {response.text}")

    # 打印分析结果
    print("\n📊 测试执行摘要")
    print(f"- 执行时间: {execution_time}")
    print(f"- 测试结果: {'通过' if is_success else '失败'}")
    print(f"- 通过: {passed_count} 个")
    print(f"- 失败: {failed_count} 个")
    print(f"- 跳过: {skipped_count} 个")

    if failed_cases:
        print("\n❌ 失败用例分析:")
        for i, case in enumerate(failed_cases, 1):
            print(f"{i}. {case['name']}")
            print(f"  - 错误类型: {case['type']}")
            print(f"  - 原因: {case['reason']}")
            print(f"  - 建议: {case['suggestion']}")

    print(f"\n✅ 结论: {'所有测试通过，接口运行正常' if is_success else '存在失败用例，请根据分析进行排查'}")


if __name__ == "__main__":
    main()
