
import json
import requests
from datetime import datetime
import pytz

beijing_tz = pytz.timezone('Asia/Shanghai')

# Test summary from pytest log
summary = {
    "passed": 69,
    "failed": 19,
    "skipped": 11
}

# List of failures
failed_cases = [
    {
        "name": "tests/test_ai配音接口测试.py::TestAi配音接口测试::test_step_02_post_voice_audition",
        "error": "AssertionError: Expected Content-Type to contain 'audio/wav', got 'application/json; charset=utf-8'",
        "type": "功能问题",
        "reason": "接口返回JSON而非音频，可能接口变更或业务逻辑错误",
        "suggestion": "检查接口返回类型"
    },
    {
        "name": "tests/test_ai配音接口测试.py::TestAi配音接口测试::test_step_05_post_voice_audition",
        "error": "AssertionError: Expected Content-Type to contain 'audio/wav', got 'application/json; charset=utf-8'",
        "type": "功能问题",
        "reason": "接口返回JSON而非音频，可能接口变更或业务逻辑错误",
        "suggestion": "检查接口返回类型"
    },
    {
        "name": "tests/test_图片克隆数字人.py::Test图片克隆数字人::test_step_03_post_human_getAlphaPhoto",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_创建手机类型对话_2d卡通.py::Test创建手机类型对话2d卡通::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建终端类型对话_2d卡通.py::Test创建终端类型对话2d卡通::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建手机类型对话.py::Test创建手机类型对话::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建终端类型对话.py::Test创建终端类型对话::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建网页类型对话.py::Test创建网页类型对话::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建终端类型对话_带动作.py::Test创建终端类型对话带动作::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_创建网页类型对话_3d数字人_带动作.py::Test创建网页类型对话3d数字人带动作::test_step_02_post_dialogs_add",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_2d视频克隆数字人.py::Test2d视频克隆数字人::test_step_02_post_human_add",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_3d形象生成.py::Test3d形象生成::test_step_02_post_human_photo_3d_gen",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_ai卡通照片接口测试.py::TestAi卡通照片接口测试::test_step_02_post_img2img_add",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_ppt讲解视频合成.py::TestPpt讲解视频合成::test_step_02_post_14_compose",
        "error": "AssertionError: Expected 200, got 503 no healthy upstream",
        "type": "环境问题",
        "reason": "上游服务不可用",
        "suggestion": "检查服务可用性"
    },
    {
        "name": "tests/test_志强基础版声音克隆.py::Test志强基础版声音克隆::test_step_02_post_voiceclone_add",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_创建网页类型对话_3d数字人.py::Test创建网页类型对话3d数字人::test_step_06_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_2d换脸克隆.py::Test2d换脸克隆::test_step_02_post_human_faceSwap",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    },
    {
        "name": "tests/test_创建网页类型对话_带动作.py::Test创建网页类型对话带动作::test_step_05_post_dialogs_get",
        "error": "AssertionError: 期望状态 'success'，实际状态 'normal'",
        "type": "测试数据问题",
        "reason": "测试用例期望的状态字段值与实际API响应不匹配",
        "suggestion": "更新测试用例状态断言"
    },
    {
        "name": "tests/test_2d离线播报数字人.py::Test2d离线播报数字人::test_step_02_post_draft_edit",
        "error": "AssertionError: Expected 200, got 504 Gateway Time-out",
        "type": "环境问题",
        "reason": "网关超时，上游服务未及时响应",
        "suggestion": "检查服务可用性和性能"
    }
]

date_str = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

# Build feishu card content
card_content = f"📊 **每日接口测试报告**\n\n"
card_content += f"**执行时间**: {date_str}\n"
card_content += f"**测试结果**: 失败\n"
card_content += f"**通过**: {summary['passed']} 个\n"
card_content += f"**失败**: {summary['failed']} 个\n"
card_content += f"**跳过**: {summary['skipped']} 个\n\n"

# Add failures
failed_section = "❌ **失败用例分析**\n"
for i, case in enumerate(failed_cases, 1):
    failed_section += f"{i}. {case['name']}\n"
    failed_section += f"   - 错误类型: {case['type']}\n"
    failed_section += f"   - 原因: {case['reason']}\n"
    failed_section += f"   - 建议: {case['suggestion']}\n\n"

card_content += failed_section
card_content += "✅ **结论**: 本次测试存在失败，主要包含环境问题（503/504）和测试数据问题（状态值不匹配），请相关人员及时排查。"

# Build feishu card json
feishu_card = {
    "msg_type": "interactive",
    "card": {
        "header": {
            "template": "red",
            "title": {
                "content": f"每日接口测试报告 - {datetime.now(beijing_tz).strftime('%Y-%m-%d')}",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": card_content,
                    "tag": "lark_md"
                }
            }
        ]
    }
}

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/90050a70-42ce-43ff-81e9-88ba482fbb70"
headers = {"Content-Type": "application/json; charset=utf-8"}
response = requests.post(webhook_url, data=json.dumps(feishu_card), headers=headers)
print("Feishu notification sent, status code:", response.status_code)
print("Response:", response.text)
