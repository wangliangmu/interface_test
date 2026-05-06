# 计划：从 Apifox 测试报告反推代码化测试用例

## 概述

使用 Playwright 自动化浏览器登录 Apifox，抓取项目 `7631843` 的测试运行报告，提取每个场景的步骤详情（请求方法、URL、Headers、Body、断言规则），然后生成 Python + pytest + requests 的代码化测试用例。

## 当前状态

- 工作区 `/workspace` 几乎为空，仅有 `README.md`（内容为 `# interface_test`）
- 无现有代码、依赖或配置
- Apifox 项目页面需要登录认证

## 技术决策

| 决策项 | 选择 |
|--------|------|
| 数据获取方式 | Playwright 抓取网页 |
| 报告类型 | 测试运行报告 |
| 测试框架 | Python + pytest + requests |
| 登录方式 | 账号密码登录（通过环境变量传入） |
| 文件组织 | 每场景一个 pytest 文件 |
| 步骤依赖 | 有依赖，需顺序执行并传递数据 |
| 断言方式 | 完整复现断言规则 |

## 实施步骤

### 步骤 1：初始化项目结构

创建 Python 项目基础结构：

```
/workspace/
├── README.md
├── requirements.txt          # 依赖：playwright, pytest, requests, jinja2
├── .env.example              # 环境变量模板（不含真实密码）
├── scraper/
│   ├── __init__.py
│   ├── login.py              # Playwright 登录逻辑
│   ├── explorer.py           # 页面探索脚本，发现报告列表和结构
│   └── extractor.py          # 从报告页面提取步骤数据
├── generator/
│   ├── __init__.py
│   └── codegen.py            # 将提取的 JSON 数据生成 pytest 测试代码
├── templates/
│   └── test_scenario.py.j2   # Jinja2 模板，生成测试文件
├── data/                     # 存放抓取的原始 JSON 数据
│   └── .gitkeep
└── tests/                    # 生成的测试用例输出目录
    └── .gitkeep
```

**依赖列表** (`requirements.txt`)：
- `playwright` - 浏览器自动化
- `pytest` - 测试框架
- `requests` - HTTP 客户端
- `jinja2` - 模板引擎，用于代码生成
- `python-dotenv` - 环境变量管理

### 步骤 2：实现 Playwright 登录模块 (`scraper/login.py`)

- 从环境变量读取 `APIFOX_PHONE` 和 `APIFOX_PASSWORD`
- 使用 Playwright 启动 Chromium（headless 模式）
- 导航到 Apifox 登录页
- 填写手机号和密码，点击登录
- 等待登录成功后保存 `storageState`（Cookie/LocalStorage）到 `data/auth_state.json`
- 后续请求复用该状态，避免重复登录

### 步骤 3：实现页面探索脚本 (`scraper/explorer.py`)

- 使用已保存的认证状态访问 `https://app.apifox.com/project/7631843`
- 探索项目页面结构，定位：
  - 测试报告入口/标签页
  - 报告列表的 DOM 结构
  - 单个报告详情页的 URL 模式
- 输出页面结构信息到 `data/page_structure.json`，供后续提取使用
- 截图保存关键页面，辅助调试

**关键**：此步骤需要实际运行 Playwright 来观察页面结构，因为 Apifox 是 SPA 应用，DOM 结构无法从静态 HTML 推断。脚本应：
1. 先截图整个页面
2. 获取页面主要元素的 HTML 结构
3. 尝试点击"测试报告"相关入口
4. 记录发现的 URL 模式和 DOM 选择器

### 步骤 4：实现数据提取模块 (`scraper/extractor.py`)

根据步骤 3 探索到的页面结构，实现：

1. **遍历报告列表**：获取所有测试运行报告的链接
2. **进入每个报告详情页**：提取场景信息
3. **提取步骤数据**：对每个场景中的每个步骤，提取：
   - 请求方法（GET/POST/PUT/DELETE 等）
   - 请求 URL（完整 URL，含 base URL 和 path）
   - 请求 Headers
   - 请求 Body（JSON/Form/Data）
   - 前置步骤的变量引用（如 `{{step1.response.body.token}}`）
   - 断言规则（状态码、响应体字段值、JSON Schema 等）
4. **保存为结构化 JSON**：输出到 `data/reports/` 目录

目标 JSON 结构：

```json
{
  "project_id": "7631843",
  "base_url": "https://xxx.com",
  "scenarios": [
    {
      "name": "场景名称",
      "report_id": "xxx",
      "steps": [
        {
          "step_index": 0,
          "name": "步骤名称",
          "method": "POST",
          "path": "/api/login",
          "headers": {"Content-Type": "application/json"},
          "body": {"username": "xxx", "password": "xxx"},
          "body_type": "json",
          "extracts": [
            {"var_name": "token", "from": "response.body.data.token"}
          ],
          "assertions": [
            {"type": "status_code", "expected": 200},
            {"type": "json_path", "path": "$.code", "expected": 0},
            {"type": "json_path", "path": "$.data.token", "operator": "not_null"}
          ]
        }
      ]
    }
  ]
}
```

### 步骤 5：实现代码生成器 (`generator/codegen.py`)

读取 `data/reports/` 下的 JSON 数据，使用 Jinja2 模板生成测试代码：

**生成逻辑**：
1. 每个场景生成一个 `test_{scenario_name}.py` 文件
2. 每个步骤生成一个测试函数 `test_step_{index}_{name}`
3. 使用 pytest 的 fixture 或模块级变量处理步骤间数据传递
4. 断言完整复现报告中的规则

**步骤间数据传递方案**：
- 使用模块级 `context` 字典存储提取的变量
- 每个步骤从 context 中读取前置步骤的输出
- 模板变量替换：`{{step1.response.body.token}}` → `context["token"]`

### 步骤 6：编写 Jinja2 模板 (`templates/test_scenario.py.j2`)

模板生成的代码结构：

```python
import pytest
import requests

BASE_URL = "{{ base_url }}"
context = {}

class Test{{ ScenarioName }}:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def test_step_01_{{ step_name }}(self):
        url = f"{BASE_URL}{{ path }}"
        # 替换模板变量
        headers = {{ headers }}
        body = {{ body }}
        response = self.session.request(
            method="{{ method }}",
            url=url,
            headers=headers,
            json=body
        )
        # 提取变量
        {% for extract in extracts %}
        self.context["{{ extract.var_name }}"] = response.json(){{ extract.json_path }}
        {% endfor %}
        # 断言
        {% for assertion in assertions %}
        {{ assertion.code }}
        {% endfor %}
```

### 步骤 7：编写主入口脚本 (`main.py`)

提供两个子命令：
- `python main.py scrape` — 执行 Playwright 抓取，保存数据到 `data/reports/`
- `python main.py generate` — 读取数据，生成测试代码到 `tests/`
- `python main.py all` — 依次执行抓取和生成

### 步骤 8：安装依赖并运行

1. `pip install -r requirements.txt`
2. `playwright install chromium`
3. 运行探索脚本，观察页面结构
4. 根据实际页面结构调整选择器
5. 运行完整抓取流程
6. 生成测试代码
7. 运行生成的测试用例验证

## 安全注意事项

- 账号密码通过 `.env` 文件传入，**不提交到 Git**
- `.gitignore` 中排除 `.env`、`data/auth_state.json`、`data/screenshots/`
- 生成的测试代码中敏感数据（密码等）也应通过环境变量传入

## 风险与应对

| 风险 | 应对 |
|------|------|
| Apifox 页面结构复杂，选择器难以定位 | 先用探索脚本截图和打印 DOM，逐步调试 |
| SPA 页面动态加载，数据可能通过 API 获取 | 监听网络请求，如果发现 API 接口则直接调用 API 获取数据 |
| 步骤间变量引用语法多样 | 先抓取实际数据，再针对性实现替换逻辑 |
| 断言规则类型多样 | 先支持常见类型（状态码、JSON Path），再逐步扩展 |

## 验证步骤

1. Playwright 能成功登录 Apifox 并保存认证状态
2. 能正确导航到测试报告页面并提取报告列表
3. 能从每个报告中提取完整的步骤数据（方法、URL、Headers、Body、断言）
4. 生成的 pytest 测试文件语法正确（可通过 `python -m py_compile` 验证）
5. 生成的测试用例能通过 `pytest --collect-only` 收集
6. 如有可用的测试环境，运行测试用例验证功能正确性
