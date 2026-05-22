
import requests
import json
from datetime import datetime, timezone
import pytz

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"

def main():
    # 执行时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    execution_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 测试结果
    passed = 91
    failed = 2
    skipped = 6
    test_result = "失败" if failed > 0 else "通过"
    
    # 失败用例分析
    failed_cases = [
        {
            "name": "test_2d离线播报数字人.test_step_04_post_video_get",
            "error_type": "功能问题",
            "reason": "接口返回状态为'producing'，期望为'normal'",
            "suggestion": "检查离线播报任务是否有超时或阻塞问题"
        },
        {
            "name": "test_志强基础版声音克隆.test_step_04_post_voiceclone_get",
            "error_type": "功能问题",
            "reason": "接口返回状态为'failed'，期望为'normal'，失败原因：声音克隆失败",
            "suggestion": "检查声音克隆服务的可用性和相关依赖"
        }
    ]
    
    # 构建卡片消息
    card_elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"📊 **测试执行摘要**\n- 执行时间: {execution_time}\n- 测试结果: {test_result}\n- 通过: {passed} 个\n- 失败: {failed} 个\n- 跳过: {skipped} 个"
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
        }
    ]
    
    for i, case in enumerate(failed_cases, 1):
        card_elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{i}. **{case['name']}**\n   - 错误类型: {case['error_type']}\n   - 原因: {case['reason']}\n   - 建议: {case['suggestion']}"
            }
        })
    
    card_elements.extend([
        {
            "tag": "hr"
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"✅ **结论**: {test_result}，请关注失败的用例"
            }
        }
    ])
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": "red" if failed > 0 else "green",
                "title": {
                    "content": f"每日接口测试报告 - {now.strftime('%Y-%m-%d')}",
                    "tag": "plain_text"
                }
            },
            "elements": card_elements
        }
    }
    
    # 发送请求
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    
    print(f"Feishu response status: {response.status_code}")
    print(f"Response content: {response.text}")

if __name__ == "__main__":
    main()
