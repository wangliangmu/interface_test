import os


def load_config(env: str = "prod") -> dict:
    configs = {
        "prod": {
            "base_url": "https://metahuman-prod.wair.ac.cn",
        },
        "staging": {
            "base_url": "https://metahuman-staging.wair.ac.cn",
        },
        "dev": {
            "base_url": "https://metahuman-dev.wair.ac.cn",
        },
    }
    return configs.get(env, configs["prod"])


BASE_URL = os.getenv("API_BASE_URL", load_config()["base_url"])

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

DEFAULT_POLL_CONFIG = {
    "max_retries": 30,
    "wait_interval": 5,
    "poll_expression": "$.data.status",
    "poll_expected_list": ["completed", "normal"],
    "error_statuses": ["failed", "error", "rejected", "timeout"]
}
