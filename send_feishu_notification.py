#!/usr/bin/env python3
import json
import requests
from datetime import datetime

def main():
    # Test results
    total_tests = 99  # 89 passed + 10 failed
    passed = 89
    failed = 10
    skipped = 0

    failure_details = [
        {
            "name": "test_创建手机类型对话",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建手机类型对话_2d卡通",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建终端类型对话",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建终端类型对话_2d卡通",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建终端类型对话_带动作",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建网页类型对话",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_创建网页类型对话_带动作",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'success'，实际状态 'failed'",
            "suggestion": "检查对话创建相关接口的业务逻辑"
        },
        {
            "name": "test_2d换脸克隆",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'normal'，实际状态 'producing'",
            "suggestion": "检查2D换脸克隆接口的处理状态逻辑"
        },
        {
            "name": "test_2d离线播报数字人",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 'normal'，实际状态 'failed'，失败原因：背景视频合成失败",
            "suggestion": "检查2D离线播报数字人背景视频合成逻辑"
        },
        {
            "name": "test_ppt讲解视频合成",
            "error_type": "功能问题",
            "reason": "解析响应或检查状态失败：期望状态 2 (成功)，实际状态 3，失败原因：PPT页面160合成失败",
            "suggestion": "检查PPT讲解视频合成逻辑"
        }
    ]

    # Generate analysis report
    report = f"""📊 测试执行摘要
- 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 测试结果: {'✅ 成功' if failed == 0 else '❌ 失败'}
- 通过: {passed} 个
- 失败: {failed} 个
- 跳过: {skipped} 个

❌ 失败用例分析:
"""
    for i, fail in enumerate(failure_details, 1):
        report += f"{i}. {fail['name']}\n"
        report += f"   - 错误类型: {fail['error_type']}\n"
        report += f"   - 原因: {fail['reason']}\n"
        report += f"   - 建议: {fail['suggestion']}\n\n"

    report += f"✅ 结论: 本次测试共执行 {total_tests} 个用例，{passed} 个通过，{failed} 个失败，请相关人员关注失败用例并及时修复。"

    print(report)

    # Send Feishu notification
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    header_template = "green" if failed == 0 else "red"
    header_title = f"每日接口测试报告 - {datetime.now().strftime('%Y-%m-%d')}"

    # Build Feishu card
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": header_template,
                "title": {
                    "content": header_title,
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": report.replace("📊", "📊 ").replace("❌", "❌ ").replace("✅", "✅ ")
                }
            ]
        }
    }

    response = requests.post(webhook_url, data=json.dumps(card), headers={"Content-Type": "application/json; charset=utf-8"})
    print("Feishu notification response:", response.status_code, response.text)

if __name__ == "__main__":
    main()
