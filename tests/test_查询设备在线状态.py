import pytest
import requests
import json
import time

from utils import resolve_template, resolve_dict, extract_json_path
from config import BASE_URL, COMMON_HEADERS, DEFAULT_POLL_CONFIG

class Test查询设备在线状态:
    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.context = {}

    def _apply_common_headers(self):
        for h in COMMON_HEADERS:
            if h.get("enable", True):
                resolved_value = resolve_template(h["value"], self.context)
                self.session.headers[h["name"]] = resolved_value

    def test_step_01_get_70fb060864924d5c89f7dc3cbb554f0d_devices(self):
        self._apply_common_headers()
        url = "https://webapi.teamviewer.com/api/v1//managed/groups/70fb0608-6492-4d5c-89f7-dc3cbb554f0d/devices/"
        url = resolve_template(url, self.context)
        headers = {}
        response = self.session.request(
            method="GET",
            url=url,
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:200]}"

