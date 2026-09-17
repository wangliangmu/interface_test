#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录并更新 apikey 脚本

功能：
1. 输入账号密码，调用 POST /metaman/api/account/login 登录，获取 JWT token
2. 携带 token 调用 POST /metaman/api/account/key（is_update=true）重新生成 apikey
3. 输出 apikey（可直接用于后续请求头 apikey）

用法：
    python update_apikey.py
    python update_apikey.py -u <username> -p <password>
    python update_apikey.py -u <username> -p <password> -e dev
    # 环境变量方式：API_BASE_URL / API_USERNAME / API_PASSWORD
"""

import argparse
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import requests

from config import BASE_URL
from utils import extract_json_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("update_apikey")

LOGIN_URL = "/metaman/api/account/login"
KEY_URL = "/metaman/api/account/key"


def parse_args():
    parser = argparse.ArgumentParser(description="登录并更新 apikey")
    parser.add_argument("-u", "--username", default=os.getenv("API_USERNAME"),
                        help="账号（默认取环境变量 API_USERNAME）")
    parser.add_argument("-p", "--password", default=os.getenv("API_PASSWORD"),
                        help="密码（默认取环境变量 API_PASSWORD）")
    parser.add_argument("-e", "--env", default="prod",
                        choices=["prod", "staging", "dev"],
                        help="环境（prod/staging/dev），默认 prod")
    parser.add_argument("--base-url", default=None,
                        help="自定义 BASE_URL（优先于 --env）")
    return parser.parse_args()


def login(session, base_url, username, password):
    url = f"{base_url}{LOGIN_URL}"
    body = {
        "source": "show",
        "username": username,
        "password": password,
        "permission": "on",
    }
    response = session.post(url, json=body)
    if response.status_code != 200:
        raise RuntimeError(f"登录失败，HTTP {response.status_code}: {response.text[:300]}")

    data = response.json()
    token = extract_json_path(data, "$.data.token")
    if not token:
        raise RuntimeError(f"登录失败，未获取到 token: {response.text[:300]}")
    logger.info("登录成功")
    return token


def update_apikey(session, base_url, token):
    url = f"{base_url}{KEY_URL}"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"is_update": True}
    response = session.post(url, json=body, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"更新 apikey 失败，HTTP {response.status_code}: {response.text[:300]}")

    data = response.json()
    code = data.get("code", -1)
    if code != 0:
        raise RuntimeError(f"更新 apikey 失败，code={code}: {response.text[:300]}")

    apikey = data.get("apikey") or extract_json_path(data, "$.data.apikey")
    if not apikey:
        raise RuntimeError(f"更新 apikey 失败，响应中无 apikey: {response.text[:300]}")
    return apikey


def main():
    args = parse_args()

    if not args.username or not args.password:
        logger.error("必须提供账号密码（-u/-p 或环境变量 API_USERNAME/API_PASSWORD）")
        sys.exit(1)

    base_url = args.base_url or os.getenv("API_BASE_URL") or BASE_URL
    logger.info("环境地址: %s", base_url)

    session = requests.Session()
    session.headers.update({"content-type": "application/json"})
    try:
        token = login(session, base_url, args.username, args.password)
        apikey = update_apikey(session, base_url, token)
    except Exception as e:
        logger.error("执行失败: %s", e)
        sys.exit(1)

    print("=" * 60)
    print(f"apikey: {apikey}")
    print("=" * 60)


if __name__ == "__main__":
    main()