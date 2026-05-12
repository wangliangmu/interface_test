#!/usr/bin/env python3
import json
import requests
from datetime import datetime


def analyze_results():
    test_time = "2026-05-12 23:16:21 - 2026-05-12 23:17:17"
    passed = 0
    failed = 26
    skipped = 72
    
    failure_details = []
    
    # 主要失败类型
    failure_details.append({
        "case": "登录接口测试",
        "error_type": "环境问题",
        "reason": "登录接口返回504 Gateway Time-out或502 Bad Gateway，服务端响应超时或不可用",
        "suggestion": "检查生产环境服务状态，排查网关或后端服务问题"
    })
    
    failure_details.append({
        "case": "语义理解服务探活",
        "error_type": "环境问题",
        "reason": "SSLError: HTTPS连接失败，SSL协议错误",
        "suggestion": "检查语义理解服务状态和SSL证书配置"
    })
    
    overall_assessment = "测试结果显示所有失败均为环境问题，服务端响应超时或服务不可用，建议优先排查生产环境服务状态。"
    
    return {
        "test_time": test_time,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "failure_details": failure_details,
        "overall_assessment": overall_assessment
    }


def build_feishu_message(result):
    date_str = datetime.now().strftime("%Y-%m-%d")
    status = "失败" if result["failed"] > 0 else "成功"
    template_color = "red" if result["failed"] > 0 else "green"
    
    # 构建摘要文本
    summary_text = f"""📊 测试执行摘要
- 执行时间: {result['test_time']}
- 测试结果: {status}
- 通过: {result['passed']} 个
- 失败: {result['failed']} 个
- 跳过: {result['skipped']} 个"""
    
    # 构建失败详情
    failure_text = ""
    if result["failure_details"]:
        failure_text = "\n❌ 失败用例分析:\n"
        for i, detail in enumerate(result["failure_details"], 1):
            failure_text += f"""{i}. {detail['case']}
  - 错误类型: {detail['error_type']}
  - 原因: {detail['reason']}
  - 建议: {detail['suggestion']}
"""
    
    conclusion_text = f"\n✅ 结论: {result['overall_assessment']}"
    
    full_text = summary_text + failure_text + conclusion_text
    
    # 构建飞书卡片消息
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": template_color,
                "title": {
                    "content": f"每日接口测试报告 - {date_str}",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": full_text
                    }
                }
            ]
        }
    }
    return card


def send_feishu_notification(webhook_url, message):
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(message),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10
        )
        response.raise_for_status()
        print(f"飞书通知发送成功: {response.text}")
        return True
    except Exception as e:
        print(f"飞书通知发送失败: {e}")
        return False


def main():
    # 分析测试结果
    result = analyze_results()
    
    # 打印分析报告
    print("=" * 80)
    print("📊 测试执行摘要")
    print(f"- 执行时间: {result['test_time']}")
    print(f"- 测试结果: {'失败' if result['failed'] > 0 else '成功'}")
    print(f"- 通过: {result['passed']} 个")
    print(f"- 失败: {result['failed']} 个")
    print(f"- 跳过: {result['skipped']} 个")
    print()
    print("❌ 失败用例分析:")
    for i, detail in enumerate(result['failure_details'], 1):
        print(f"{i}. {detail['case']}")
        print(f"  - 错误类型: {detail['error_type']}")
        print(f"  - 原因: {detail['reason']}")
        print(f"  - 建议: {detail['suggestion']}")
        print()
    print(f"✅ 结论: {result['overall_assessment']}")
    print("=" * 80)
    
    # 发送飞书通知
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
    message = build_feishu_message(result)
    send_feishu_notification(webhook_url, message)


if __name__ == "__main__":
    main()
