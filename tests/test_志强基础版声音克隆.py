import pytest
import requests
import json
import re
import time
from datetime import datetime

BASE_URL = "https://metahuman-prod.wair.ac.cn"
COMMON_HEADERS = [
    {
        "name": "token",
        "value": "{{token}}",
        "enable": True
    },
    {
        "name": "Authorization",
        "value": "Bearer {{token}}",
        "enable": True
    },
    {
        "name": "auto-gen-qa-tasks_id",
        "value": "{{auto-gen-qa-tasks_id}}",
        "enable": True
    }
]


def resolve_template(text, context):
    if not isinstance(text, str):
        return text
    def replacer(match):
        var_name = match.group(1)
        if var_name.startswith("$date"):
            return datetime.now().strftime("%m%d_%H%M")
        if var_name in context:
            return str(context[var_name])
        return match.group(0)
    return re.sub(r'\{\{(\S+?)\}\}', replacer, text)


def resolve_dict(d, context):
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            if isinstance(v, str):
                import re
                match = re.search(r'\{\{(\w+)\}\}', v)
                if match:
                    var_name = match.group(1)
                    result[k] = context.get(var_name, v)
                else:
                    result[k] = resolve_template(v, context)
            else:
                result[k] = resolve_dict(v, context)
        return result
    elif isinstance(d, list):
        return [resolve_dict(v, context) for v in d]
    elif isinstance(d, str):
        return resolve_template(d, context)
    return d


def extract_json_path(data, path):
    import jsonpath_ng
    expr = jsonpath_ng.parse(path)
    matches = expr.find(data)
    if matches:
        return matches[0].value
    return None


class Test志强基础版声音克隆:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_post_account_login(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/account/login"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "source": "show",
    "username": "auto_test_jxm",
    "password": "auto_test_jxm123",
    "permission": "on"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["token"] = extract_json_path(response.json(), "$.data.token")
        except Exception:
            self.context["token"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_02_post_voiceclone_add(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/add"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "测试1",
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/9756fa15-aca9-4dc6-b99a-3db855f3ceec.wav"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["voice_clone_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["voice_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_voiceclone_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/voiceclone/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "id": "{{voice_clone_id}}"
}
        body = resolve_dict(body, self.context)
        
        max_retries = 60
        wait_interval = 5
        poll_expression = "$.data.status"
        poll_expected = "completed"
        error_statuses = ["failed", "error", "rejected", "timeout"]
        
        for attempt in range(max_retries):
            response = self.session.request(
                method="POST",
                url=url,
                json=body,
                headers=headers,
            )
            
            if response.status_code != 200:
                print(f"Poll attempt {attempt+1}/{max_retries}: HTTP {response.status_code}")
                time.sleep(wait_interval)
                continue
            
            try:
                data = response.json()
                actual_value = extract_json_path(data, poll_expression)
                
                if actual_value == poll_expected:
                    print(f"Poll attempt {attempt+1}/{max_retries}: Task completed successfully")
                    break
                    
                if actual_value in error_statuses:
                    raise RuntimeError(f"Task failed with status: {actual_value}")
                    
                print(f"Poll attempt {attempt+1}/{max_retries}: Current status = {actual_value!r}, waiting...")
                
            except json.JSONDecodeError:
                print(f"Poll attempt {attempt+1}/{max_retries}: Failed to parse JSON response")
            except Exception as e:
                print(f"Poll attempt {attempt+1}/{max_retries}: Error - {str(e)}")
            
            time.sleep(wait_interval)
        else:
            raise TimeoutError(f"Polling timeout after {max_retries * wait_interval} seconds")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

