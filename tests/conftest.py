import pytest
import requests

from .config import BASE_URL, COMMON_HEADERS
from .utils import resolve_template, resolve_dict, extract_json_path


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "clone: 克隆相关测试")
    config.addinivalue_line("markers", "ai: AI功能测试")
    config.addinivalue_line("markers", "dialog: 对话创建测试")
    config.addinivalue_line("markers", "login: 登录测试")
    config.addinivalue_line("markers", "risk: 风控测试")


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
