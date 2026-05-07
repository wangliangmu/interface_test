import os
import html as html_lib
import pytest
import requests

from config import BASE_URL, COMMON_HEADERS
from utils import resolve_template, resolve_dict, extract_json_path, LoggingSession


_class_results = {}


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "clone: 克隆相关测试")
    config.addinivalue_line("markers", "ai: AI功能测试")
    config.addinivalue_line("markers", "dialog: 对话创建测试")
    config.addinivalue_line("markers", "login: 登录测试")
    config.addinivalue_line("markers", "risk: 风控测试")


def pytest_sessionstart(session):
    requests.Session = LoggingSession


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    class_name = item.cls.__name__ if item.cls else item.module.__name__
    file_name = os.path.basename(str(item.module.__file__))
    if class_name not in _class_results:
        _class_results[class_name] = {
            "file": file_name,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "total": 0,
            "failed_tests": [],
        }
    entry = _class_results[class_name]
    entry["total"] += 1

    if report.passed:
        entry["passed"] += 1
    elif report.failed:
        entry["failed"] += 1
        entry["failed_tests"].append(item.name)
    elif report.skipped:
        entry["skipped"] += 1

    if hasattr(report, "longrepr") and report.longrepr:
        if report.outcome == "error" or (report.failed and call.excinfo and call.excinfo.typename != "AssertionError"):
            entry["errors"] += 1


def pytest_sessionfinish(session, exitstatus):
    if not _class_results:
        return

    reports_dir = os.path.join(str(session.config.rootdir), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"summary_{timestamp}.html")

    total_classes = len(_class_results)
    total_passed = sum(v["passed"] for v in _class_results.values())
    total_failed = sum(v["failed"] for v in _class_results.values())
    total_skipped = sum(v["skipped"] for v in _class_results.values())
    total_tests = sum(v["total"] for v in _class_results.values())
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    rows_html = ""
    for idx, (cls_name, data) in enumerate(_class_results.items(), 1):
        cls_pass_rate = (data["passed"] / data["total"] * 100) if data["total"] > 0 else 0
        status_class = "status-pass" if data["failed"] == 0 and data["errors"] == 0 else "status-fail"
        status_text = "通过" if data["failed"] == 0 and data["errors"] == 0 else "失败"
        failed_tests_html = ""
        if data["failed_tests"]:
            items = "".join(f"<li>{html_lib.escape(t)}</li>" for t in data["failed_tests"])
            failed_tests_html = f'<ul class="failed-list">{items}</ul>'

        rows_html += f"""
        <tr class="{status_class}">
            <td>{idx}</td>
            <td class="cls-name">{html_lib.escape(cls_name)}</td>
            <td>{html_lib.escape(data["file"])}</td>
            <td>{data["total"]}</td>
            <td class="pass">{data["passed"]}</td>
            <td class="fail">{data["failed"]}</td>
            <td>{data["skipped"]}</td>
            <td>{cls_pass_rate:.1f}%</td>
            <td><span class="badge {status_class}">{status_text}</span></td>
            <td>{failed_tests_html}</td>
        </tr>"""

    overall_status = "全部通过" if total_failed == 0 else f"{total_failed} 个失败"
    overall_class = "status-pass" if total_failed == 0 else "status-fail"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>接口测试报告 - 按测试类汇总</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f5f7fa; color: #333; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; font-size: 24px; margin-bottom: 8px; color: #1a1a2e; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 24px; font-size: 14px; }}
        .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .card {{ background: #fff; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .card .value {{ font-size: 32px; font-weight: 700; }}
        .card .label {{ font-size: 13px; color: #888; margin-top: 4px; }}
        .card.total .value {{ color: #1a1a2e; }}
        .card.pass .value {{ color: #27ae60; }}
        .card.fail .value {{ color: #e74c3c; }}
        .card.skip .value {{ color: #f39c12; }}
        .card.rate .value {{ color: #2980b9; }}
        .overall {{ background: #fff; border-radius: 8px; padding: 16px 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); display: flex; justify-content: space-between; align-items: center; }}
        .overall .status {{ font-size: 20px; font-weight: 700; }}
        .overall.status-pass .status {{ color: #27ae60; }}
        .overall.status-fail .status {{ color: #e74c3c; }}
        table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        th {{ background: #1a1a2e; color: #fff; padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 600; }}
        td {{ padding: 10px 16px; border-bottom: 1px solid #eee; font-size: 13px; }}
        tr:hover {{ background: #f8f9fa; }}
        tr.status-pass:hover {{ background: #f0fff4; }}
        tr.status-fail:hover {{ background: #fff5f5; }}
        .cls-name {{ font-weight: 600; color: #1a1a2e; }}
        .pass {{ color: #27ae60; font-weight: 600; }}
        .fail {{ color: #e74c3c; font-weight: 600; }}
        .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .badge.status-pass {{ background: #d4edda; color: #155724; }}
        .badge.status-fail {{ background: #f8d7da; color: #721c24; }}
        .failed-list {{ margin: 0; padding-left: 16px; font-size: 12px; color: #e74c3c; }}
        .failed-list li {{ margin-bottom: 2px; }}
        .footer {{ text-align: center; margin-top: 24px; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>接口测试报告</h1>
        <p class="subtitle">按测试类汇总 | 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="summary-cards">
            <div class="card total">
                <div class="value">{total_classes}</div>
                <div class="label">测试类数</div>
            </div>
            <div class="card total">
                <div class="value">{total_tests}</div>
                <div class="label">用例总数</div>
            </div>
            <div class="card pass">
                <div class="value">{total_passed}</div>
                <div class="label">通过</div>
            </div>
            <div class="card fail">
                <div class="value">{total_failed}</div>
                <div class="label">失败</div>
            </div>
            <div class="card skip">
                <div class="value">{total_skipped}</div>
                <div class="label">跳过</div>
            </div>
            <div class="card rate">
                <div class="value">{pass_rate:.1f}%</div>
                <div class="label">通过率</div>
            </div>
        </div>

        <div class="overall {overall_class}">
            <div class="status">{overall_status}</div>
            <div>共 {total_classes} 个测试类，{total_tests} 个用例</div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>测试类</th>
                    <th>文件</th>
                    <th>总数</th>
                    <th>通过</th>
                    <th>失败</th>
                    <th>跳过</th>
                    <th>通过率</th>
                    <th>状态</th>
                    <th>失败用例</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <p class="footer">接口测试框架 | 自动生成</p>
    </div>
</body>
</html>"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n按类汇总报告: {report_path}")


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"content-type": "application/json"})
    yield session
    session.close()


@pytest.fixture(scope="session")
def test_context():
    return {}


@pytest.fixture(scope="session")
def authenticated_session(api_session, test_context):
    url = f"{BASE_URL}/metaman/api/account/login"
    body = {
        "source": "show",
        "username": "auto_test_jxm",
        "password": "auto_test_jxm123",
        "permission": "on"
    }

    response = api_session.request(
        method="POST",
        url=url,
        json=body,
    )

    assert response.status_code == 200, f"登录失败: {response.text[:200]}"

    try:
        test_context["token"] = extract_json_path(response.json(), "$.data.token")
    except Exception as e:
        pytest.fail(f"提取 token 失败: {e}")

    for h in COMMON_HEADERS:
        if h.get("enable", True):
            resolved_value = resolve_template(h["value"], test_context)
            api_session.headers[h["name"]] = resolved_value

    return api_session
