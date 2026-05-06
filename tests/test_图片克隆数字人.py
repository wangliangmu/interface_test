import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path, poll_until
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

@pytest.mark.smoke
@pytest.mark.clone
class Test图片克隆数字人:
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

    def test_step_02_post_risk_check(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/tool/risk/check"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "content": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/15b98bb8-376c-430f-b97e-5bb6f016f7ec.jpg",
    "type": "image"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_03_post_human_getAlphaPhoto(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/getAlphaPhoto"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/15b98bb8-376c-430f-b97e-5bb6f016f7ec.jpg"
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    def test_step_04_post_human_photoClone(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/photoClone"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "name": "图片克隆{{$date.now|format('MMdd_HHmm')}}",
    "src_path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/photo/233/22ac2320-3103-43e4-b273-1c412141489d.jpg",
    "alpha_path": "https://s3-h20.wair.ac.cn/alluxio/metaman/metaman/video/233/9c20e09f-ba7f-4672-9946-77b41c44f299.png",
    "bUsed": True
}
        body = resolve_dict(body, self.context)
        response = self.session.request(
            method="POST",
            url=url,
            json=body,
            headers=headers,
        )
        try:
            self.context["photo_clone_id"] = extract_json_path(response.json(), "$.data.id")
        except Exception:
            self.context["photo_clone_id"] = None
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

    @pytest.mark.skip(reason="Task takes too long to complete, marked as skipped temporarily")
    def test_step_06_post_human_get(self):
        self._apply_common_headers()
        url = f"{BASE_URL}/metaman/api/asset/human/get"
        url = resolve_template(url, self.context)
        headers = {
    "content-type": "application/json",
    "priority": "u=1, i"
}
        headers = resolve_dict(headers, self.context)
        body = {
    "human_id": "{{photo_clone_id}}"
}
        body = resolve_dict(body, self.context)
        response = poll_until(self.session, url, body, headers, DEFAULT_POLL_CONFIG, self.context)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

