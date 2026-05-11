import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import pytest

from .base_test import BaseTest
from config import BASE_URL
from utils import extract_json_path

logger = logging.getLogger("api_test")


@pytest.mark.smoke
@pytest.mark.login
class Test登录(BaseTest):
    def test_step_01_post_account_login(self):
        self._login()