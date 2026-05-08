# 接口测试框架

基于 pytest 的接口自动化测试框架，支持日志记录、并行执行、HTML 报告生成等功能。

## 项目结构

```
interface_test/
├── config.py           # 全局配置（环境、请求头、轮询配置）
├── utils.py            # 工具函数（日志、模板解析、轮询）
├── run_tests.py        # 测试入口脚本
├── pytest.ini          # pytest 配置文件
├── requirements.txt     # 项目依赖
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略配置
└── tests/              # 测试用例目录
    ├── conftest.py      # pytest fixtures 和钩子
    ├── __init__.py
    └── test_*.py         # 各模块测试用例（26个测试文件，105个测试函数）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

复制环境变量配置文件：

```bash
cp .env.example .env
```

根据需要编辑 `.env` 或设置环境变量 `API_BASE_URL`。

### 3. 运行测试

```bash
# 运行所有测试（默认配置）
python run_tests.py

# 并行执行所有测试
python run_tests.py -p

# 只运行冒烟测试
python run_tests.py -m smoke

# 生成 HTML 报告和日志文件
python run_tests.py --html --log

# 查看帮助
python run_tests.py --help
```

## 入口脚本参数

| 参数 | 说明 |
|------|------|
| `test_path` | 指定测试路径（文件或目录） |
| `-m, --marker` | 按标记筛选测试（smoke, clone, ai, dialog, login, risk） |
| `-p, --parallel` | 启用并行执行 |
| `-w, --workers` | 指定并行 worker 数量（如：4, auto） |
| `--rerun N` | 失败用例重试 N 次 |
| `-x, --failfast` | 遇到第一个失败即停止 |
| `--html` | 生成 HTML 测试报告 |
| `--junit` | 生成 JUnit XML 报告（CI 集成用） |
| `--coverage` | 生成代码覆盖率报告 |
| `-l, --log` | 生成详细的日志文件 |
| `-v, --verbose` | 详细输出模式（-vv） |
| `-q, --quiet` | 安静模式，减少输出 |
| `--collect-only` | 只收集测试用例，不执行 |

## 测试用例分类

| 标记 | 说明 | 测试文件数 |
|------|------|------------|
| `smoke` | 冒烟测试 | 1 |
| `clone` | 克隆相关测试 | 1 |
| `ai` | AI 功能测试 | 4 |
| `dialog` | 对话创建测试 | 10 |
| `login` | 登录测试 | 1 |
| `risk` | 风控测试 | 1 |

### 全部测试用例（共 26 个测试文件，103 个测试函数）

- `test_登录.py` - 登录接口测试
- `test_首页接口测试.py` - 首页接口测试
- `test_2d换脸克隆.py` - 2D 换脸克隆
- `test_2d离线播报数字人.py` - 2D 离线播报数字人
- `test_2d视频克隆数字人.py` - 2D 视频克隆数字人
- `test_3d形象生成.py` - 3D 形象生成
- `test_ai卡通照片接口测试.py` - AI 卡通照片
- `test_ai职业照接口测试.py` - AI 职业照
- `test_ai配音接口测试.py` - AI 配音
- `test_ppt讲解视频合成.py` - PPT 讲解视频合成
- `test_图片克隆数字人.py` - 图片克隆数字人
- `test_志强基础版声音克隆.py` - 声音克隆
- `test_精品克隆音频检测接口测试.py` - 音频检测
- `test_创建手机类型对话.py` - 手机类型对话
- `test_创建手机类型对话_2d卡通.py` - 手机类型 2D 对话
- `test_创建终端类型对话.py` - 终端类型对话
- `test_创建终端类型对话_2d卡通.py` - 终端类型 2D 对话
- `test_创建终端类型对话_带动作.py` - 终端类型带动作对话
- `test_创建网页类型对话.py` - 网页类型对话
- `test_创建网页类型对话_3d数字人.py` - 网页类型 3D 对话
- `test_创建网页类型对话_3d数字人_带动作.py` - 网页类型 3D 带动作对话
- `test_创建网页类型对话_带动作.py` - 网页类型带动作对话
- `test_创建语音聊天对话.py` - 语音聊天对话
- `test_自主创建faq.py` - 自主创建 FAQ
- `test_语义理解服务探活.py` - 语义理解服务探活
- `test_风控测试.py` - 风控测试

## 核心模块说明

### config.py - 全局配置

```python
# 环境配置
BASE_URL = "https://metahuman-prod.wair.ac.cn"  # 可通过 API_BASE_URL 环境变量覆盖

# 通用请求头（支持模板变量）
COMMON_HEADERS = [
    {"name": "token", "value": "{{token}}", "enable": True},
    {"name": "Authorization", "value": "Bearer {{token}}", "enable": True},
]

# 轮询配置
DEFAULT_POLL_CONFIG = {
    "max_retries": 120,           # 最大重试次数
    "wait_interval": 5,            # 重试间隔（秒）
    "poll_expression": "$.data.status",  # JSONPath 表达式
    "poll_expected_list": ["completed", "normal", "success"],  # 成功状态
    "error_statuses": ["failed", "error", "rejected", "timeout", "canceled"]  # 失败状态
}
```

### utils.py - 工具函数

#### LoggingSession - 自动日志记录

自动记录每个 HTTP 请求的详细信息：

- **Request 日志**：HTTP 方法、URL、请求头（脱敏）、请求体（JSON 格式化）
- **Response 日志**：状态码、耗时（ms）、响应头（脱敏）、响应体（JSON 格式化）
- **敏感信息脱敏**：`Authorization`、`Token`、`Cookie` 等自动遮掩
- **大响应截断**：响应体超过 5000 字符自动截断

示例日志输出：

```
2026-05-07 06:38:19 [INFO] api_test - ================================================================================
2026-05-07 06:38:19 [INFO] api_test - REQUEST >>> POST https://metahuman-prod.wair.ac.cn/metaman/api/account/login
2026-05-07 06:38:19 [INFO] api_test - Request Headers:
{
  "content-type": "application/json",
  "Authorization": "****_123"
}
2026-05-07 06:38:19 [INFO] api_test - Request Body:
{
  "source": "show",
  "username": "auto_test_jxm",
  "password": "auto_test_jxm123"
}
2026-05-07 06:38:20 [INFO] api_test - RESPONSE <<< 200 (耗时: 1147ms)
2026-05-07 06:38:20 [INFO] api_test - Response Body:
{
  "code": 0,
  "data": { "token": "xxx" }
}
2026-05-07 06:38:20 [INFO] api_test - ================================================================================
```

#### 模板变量

支持 `{{variable}}` 语法动态替换：

```python
body = {
    "name": "2D换脸{{$date.now}}",  # 自动替换为当前日期时间
    "human_id": "{{faceswap_task_id}}"  # 引用上下文变量
}
```

#### resolve_dict() - 深度模板解析

递归解析字典中的模板变量，支持类型自动转换：

```python
resolve_dict({
    "id": 123,              # 保持原值
    "name": "{{username}}",  # 替换为上下文值
    "enabled": "{{is_active}}"  # "true" -> True (布尔转换)
}, context)
```

#### extract_json_path() - JSONPath 提取

使用 JSONPath 表达式从响应中提取数据：

```python
token = extract_json_path(response.json(), "$.data.token")
```

#### poll_until() - 轮询等待

等待异步任务完成：

```python
response = poll_until(
    session=session,
    url=f"{BASE_URL}/api/asset/human/get",
    body={"human_id": "{{faceswap_task_id}}"},
    headers={},
    poll_config=DEFAULT_POLL_CONFIG,
    context=self.context
)
```

### conftest.py - pytest 配置

#### Fixtures

- `api_session` - 基础 Session fixture
- `test_context` - 测试上下文（存储变量）
- `authenticated_session` - 已认证的 Session（自动登录获取 token）

#### 自动日志集成

通过 `pytest_sessionstart` 钩子自动将 `requests.Session` 替换为 `LoggingSession`，无需修改任何测试代码即可获得完整的请求/响应日志。

## 测试用例编写规范

### 基础结构

```python
import pytest
from utils import resolve_template, resolve_dict, extract_json_path, poll_until
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

class Test模块名:
    @classmethod
    def setup_class(cls):
        cls.session = pytest.Session.request  # 自动使用 LoggingSession
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_操作名称(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/..."
        body = {
            "key": "value",
            "template": "{{variable}}"
        }
        body = resolve_dict(body, self.context)
        response = self.session.request(method="POST", url=url, json=body)
        # 提取结果供后续步骤使用
        self.context["result_id"] = extract_json_path(response.json(), "$.data.id")
        assert response.status_code == 200
```

### 带轮询的异步任务

```python
def test_step_04_post_任务查询(self):
    self._apply_common_headers()
    url = f"{BASE_URL}/metaman/api/asset/human/get"
    body = {"human_id": "{{task_id}}"}
    body = resolve_dict(body, self.context)
    response = poll_until(self.session, url, body, {}, DEFAULT_POLL_CONFIG, self.context)
    assert response.status_code == 200
```

## 日志和报告

### 输出目录

```
reports/
├── report_20260507_065910.html   # HTML 测试报告
└── junit_20260507_065910.xml      # JUnit XML 报告

logs/
└── test_20260507_065910.log       # 详细日志文件
```

### pytest.ini 配置

```ini
[pytest]
addopts = -v --tb=short -n auto --dist=loadscope
testpaths = ["tests"]
log_cli = true
log_cli_level = INFO
log_file = api_test.log
log_file_level = DEBUG
```

## 环境说明

| 环境 | Base URL |
|------|----------|
| 生产环境 (prod) | https://metahuman-prod.wair.ac.cn |
| 预发环境 (staging) | https://metahuman-staging.wair.ac.cn |
| 开发环境 (dev) | https://metahuman-dev.wair.ac.cn |

默认使用生产环境，可通过环境变量 `API_BASE_URL` 覆盖。

## 依赖说明

| 依赖 | 版本 | 说明 |
|------|------|------|
| pytest | >=7.0.0 | 测试框架 |
| requests | >=2.28.0 | HTTP 客户端 |
| jsonpath-ng | >=1.5.0 | JSONPath 解析 |
| pytest-html | >=3.2.0 | HTML 报告 |
| pytest-xdist | >=3.0.0 | 并行执行 |
| pytest-rerunfailures | >=11.0 | 失败重试 |
| pytest-cov | >=4.0.0 | 覆盖率统计 |
| pytest-reportlog | >=0.1.0 | 日志报告 |

## 常见问题

### Q: 如何调试某个失败的测试？

```bash
# 使用 -x 遇到第一个失败就停止
python run_tests.py -x

# 使用 -v --tb=long 获取更详细的错误信息
python run_tests.py -v --tb=long tests/具体文件.py
```

### Q: 如何只运行某个测试文件？

```bash
python run_tests.py tests/test_登录.py
```

### Q: 如何并行执行测试？

```bash
# 自动检测 CPU 核心数
python run_tests.py -p

# 指定 4 个 worker
python run_tests.py -p -w 4
```

### Q: 如何处理不稳定的测试？

```bash
# 失败自动重试 2 次
python run_tests.py --rerun 2

# 组合使用
python run_tests.py -p --rerun 3
```

## License

Private - Internal Use Only
