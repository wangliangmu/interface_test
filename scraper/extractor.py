import os
import json
import re
import time
from pathlib import Path
import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = DATA_DIR / "reports"
AUTH_STATE_PATH = DATA_DIR / "auth_state.json"
PROJECT_ID = 7631843
API_BASE = f"https://api.apifox.com/api/v1/projects/{PROJECT_ID}"
CASES_API_BASE = "https://api.apifox.com/api/v1/api-test/cases"


def _get_session():
    with open(AUTH_STATE_PATH, "r") as f:
        state = json.load(f)

    cookies = state.get("cookies", [])
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    device_id = ""
    for c in cookies:
        if c["name"] == "projectCid":
            device_id = c["value"]
            break

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US",
        "Referer": "https://app.apifox.com/",
        "Cookie": cookie_str,
        "x-branch-id": "7371734",
        "x-client-mode": "web",
        "x-client-version": "2.8.27-alpha.1",
        "x-device-id": device_id,
        "x-project-id": str(PROJECT_ID),
        "access-control-allow-origin": "*",
    })
    return session


def fetch_scenario_tree(session):
    url = f"{API_BASE}/test-scenario/tree-list?locale=en-US"
    resp = session.get(url, timeout=30)
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Failed to fetch scenario tree: {data.get('errorMessage')}")
    return data["data"]


def fetch_environments(session):
    url = f"{API_BASE}/environments?locale=en-US"
    resp = session.get(url, timeout=30)
    data = resp.json()
    if data.get("success"):
        return data.get("data", [])
    return []


def fetch_global_variables(session):
    url = "https://api.apifox.com/api/v1/global-variables?locale=en-US"
    resp = session.get(url, timeout=30)
    data = resp.json()
    if data.get("success"):
        return data.get("data", [])
    return []


def fetch_common_parameters(session):
    url = f"{API_BASE}/common-parameters?locale=en-US"
    resp = session.get(url, timeout=30)
    data = resp.json()
    if data.get("success"):
        return data.get("data", [])
    return []


def fetch_scenario_steps(session, scenario_id):
    url = f"{CASES_API_BASE}/{scenario_id}/steps?withCaseDetail=true&locale=en-US"
    resp = session.get(url, timeout=60)
    result = resp.json()
    if not result.get("success"):
        print(f"    Warning: Failed to fetch steps for scenario {scenario_id}: {result.get('errorMessage')}")
        return None
    return result.get("data")


def parse_step(step_data):
    step_type = step_data.get("type", "")
    if step_type == "customHttp":
        req = step_data.get("customHttpRequest", {})
        return parse_http_step(req)
    elif step_type == "wait":
        return {
            "type": "wait",
            "duration": step_data.get("wait", {}).get("duration", 1000),
        }
    elif step_type == "conditional":
        return {
            "type": "conditional",
            "condition": step_data.get("condition", {}),
        }
    else:
        return {"type": step_type, "raw": step_data}


def parse_http_step(req):
    method = req.get("method", "get").upper()
    path = req.get("path", "")
    name = req.get("name", path)

    headers = []
    for h in req.get("parameters", {}).get("header", []):
        if h.get("enable", True):
            headers.append({
                "name": h["name"],
                "value": replace_template_vars(h.get("value", "")),
                "sample_value": replace_template_vars(h.get("sampleValue", "")),
            })

    for h in req.get("commonParameters", {}).get("header", []):
        if h.get("enable", True):
            headers.append({
                "name": h["name"],
                "value": replace_template_vars(h.get("value", "")),
                "sample_value": replace_template_vars(h.get("sampleValue", "")),
            })

    body = {}
    request_body = req.get("requestBody", {})
    if request_body:
        body_type = request_body.get("type", "")
        body_data = request_body.get("data", request_body.get("example", ""))
        if body_data:
            if body_type == "application/json":
                try:
                    body = json.loads(body_data)
                except json.JSONDecodeError:
                    sanitized = re.sub(r'\{\{([^}]+)\}\}', r'"__TPL__\1__TPL__"', body_data)
                    try:
                        body = json.loads(sanitized)
                        def restore_templates(obj):
                            if isinstance(obj, str):
                                m = re.match(r'^__TPL__(.+)__TPL__$', obj)
                                if m:
                                    return "{{" + m.group(1) + "}}"
                                return re.sub(r'__TPL__(.+?)__TPL__', r'{{\1}}', obj)
                            elif isinstance(obj, dict):
                                return {k: restore_templates(v) for k, v in obj.items()}
                            elif isinstance(obj, list):
                                return [restore_templates(v) for v in obj]
                            return obj
                        body = restore_templates(body)
                    except json.JSONDecodeError:
                        body = {"_raw": replace_template_vars(body_data)}
            else:
                body = {"_raw": replace_template_vars(body_data), "_type": body_type}

    extracts = []
    for pp in req.get("postProcessors", []):
        if pp.get("type") == "extractor" and pp.get("enable", True):
            ext_data = pp.get("data", {})
            extracts.append({
                "variable_name": ext_data.get("variableName", ""),
                "variable_type": ext_data.get("variableType", "local"),
                "expression": ext_data.get("expression", ""),
                "subject": ext_data.get("subject", "responseJson"),
            })

    assertions = []
    for pp in req.get("postProcessors", []):
        if pp.get("type") == "assertion" and pp.get("enable", True):
            assertions.append(pp.get("data", {}))

    return {
        "type": "http",
        "name": name,
        "method": method,
        "path": path,
        "headers": headers,
        "body": body,
        "extracts": extracts,
        "assertions": assertions,
    }


def replace_template_vars(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\{\{\$date\.now\|format\([\'"]([^\'"]+)[\'"]\)\}\}', 
                  'DATE_FORMAT_PLACEHOLDER', text)
    text = re.sub(r'\{\{(\w+)\}\}', r'{{\1}}', text)
    return text


def fetch_all_data():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    session = _get_session()

    print("Fetching scenario tree...")
    tree_data = fetch_scenario_tree(session)
    scenarios = tree_data.get("testScenarios", [])
    folders = tree_data.get("testScenarioFolders", [])
    folder_map = {f["id"]: f["name"] for f in folders}
    print(f"Found {len(scenarios)} scenarios in {len(folders)} folders")

    print("Fetching environments...")
    environments = fetch_environments(session)
    with open(REPORTS_DIR / "environments.json", "w", encoding="utf-8") as f:
        json.dump(environments, f, ensure_ascii=False, indent=2)

    base_url = ""
    for env in environments:
        if "正式" in env.get("name", ""):
            base_url = env.get("baseUrl", env.get("baseUrls", {}).get("default", ""))
            break
    if not base_url and environments:
        base_url = environments[0].get("baseUrl", environments[0].get("baseUrls", {}).get("default", ""))
    print(f"Base URL: {base_url}")

    print("Fetching common parameters...")
    common_params = fetch_common_parameters(session)
    with open(REPORTS_DIR / "common_parameters.json", "w", encoding="utf-8") as f:
        json.dump(common_params, f, ensure_ascii=False, indent=2)

    common_headers = []
    if isinstance(common_params, dict):
        for p in common_params.get("parameters", {}).get("header", []):
            common_headers.append({
                "name": p.get("name", ""),
                "value": p.get("defaultValue", p.get("schema", {}).get("default", "")),
                "enable": p.get("defaultEnable", True),
            })
    print(f"Common headers: {len(common_headers)}")

    print("Fetching scenario steps...")
    all_scenarios = []
    for i, scenario in enumerate(scenarios):
        sid = scenario["id"]
        name = scenario.get("name", "")
        folder_id = scenario.get("folderId", 0)
        folder_name = folder_map.get(folder_id, "")

        print(f"  [{i+1}/{len(scenarios)}] {name} (id={sid})")

        detail = fetch_scenario_steps(session, sid)
        if detail is None:
            continue

        steps = []
        for step_data in detail.get("steps", []):
            if step_data.get("disable", False):
                continue
            parsed = parse_step(step_data)
            if parsed:
                steps.append(parsed)

        scenario_info = {
            "id": sid,
            "name": name,
            "folder_name": folder_name,
            "folder_id": folder_id,
            "priority": scenario.get("priority", 2),
            "tags": scenario.get("tags", []),
            "steps": steps,
        }
        all_scenarios.append(scenario_info)

        time.sleep(0.3)

    project_data = {
        "project_id": PROJECT_ID,
        "base_url": base_url,
        "environments": [{"id": e["id"], "name": e["name"], "baseUrl": e.get("baseUrl", "")} for e in environments],
        "common_headers": common_headers,
        "scenarios": all_scenarios,
    }

    output_path = REPORTS_DIR / "project_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

    print(f"\nData saved to {output_path}")
    print(f"Total scenarios with steps: {len([s for s in all_scenarios if s['steps']])}")
    print(f"Total steps: {sum(len(s['steps']) for s in all_scenarios)}")

    return project_data


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    fetch_all_data()
