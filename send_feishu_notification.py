#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import pytz

# 测试数据
test_date = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
execution_time = '2026-05-19 07:17:13'
total_tests = 99
passed = 98
failed = 1
skipped = 0

# 失败用例分析
failed_cases = [
    {
        'name': 'tests/test_创建网页类型对话.py::Test创建网页类型对话::test_step_05_post_dialogs_get',
        'error_type': '功能问题',
        'reason': '合成播报视频失败，任务状态最终为 failed',
        'suggestion': '检查播报视频合成服务的健康状态，查看相关日志定位失败原因'
    }
]

# 构建 Feishu 卡片消息
feishu_webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70'

# 卡片模板
card = {
    'msg_type': 'interactive',
    'card': {
        'config': {
            'wide_screen_mode': True
        },
        'header': {
            'template': 'red' if failed > 0 else 'green',
            'title': {
                'tag': 'plain_text',
                'content': f'每日接口测试报告 - {test_date}'
            }
        },
        'elements': [
            {
                'tag': 'div',
                'text': {
                    'tag': 'lark_md',
                    'content': f'**📊 测试执行摘要**\n- 执行时间: {execution_time}\n- 测试结果: {"失败" if failed > 0 else "通过"}\n- 通过: {passed} 个\n- 失败: {failed} 个\n- 跳过: {skipped} 个'
                }
            },
            {
                'tag': 'hr'
            }
        ]
    }
}

# 添加失败用例分析
if failed > 0:
    card['card']['elements'].append({
        'tag': 'div',
        'text': {
            'tag': 'lark_md',
            'content': '**❌ 失败用例分析**'
        }
    })
    for i, case in enumerate(failed_cases, 1):
        card['card']['elements'].append({
            'tag': 'div',
            'text': {
                'tag': 'lark_md',
                'content': f'{i}. **{case["name"]}**\n- 错误类型: {case["error_type"]}\n- 原因: {case["reason"]}\n- 建议: {case["suggestion"]}'
            }
        })
        if i < len(failed_cases):
            card['card']['elements'].append({'tag': 'hr'})

# 添加结论
card['card']['elements'].extend([
    {
        'tag': 'hr'
    },
    {
        'tag': 'div',
        'text': {
            'tag': 'lark_md',
            'content': f'**✅ 结论**: 本次测试执行完成，共 {total_tests} 个用例，{passed} 个通过，{failed} 个失败'
        }
    }
])

# 发送请求
response = requests.post(
    feishu_webhook,
    headers={'Content-Type': 'application/json; charset=utf-8'},
    data=json.dumps(card)
)

print(f'Status code: {response.status_code}')
print(f'Response: {response.text}')
