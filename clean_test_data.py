import requests
from datetime import datetime, timedelta

API_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/human/list"
DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/human/delete"
VOICE_LIST_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/voice/userlist"
VOICE_DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/voice/delete"
AI_LIST_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/ai/list"
AI_DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/ai/delete"
LOGIN_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/account/login"

TOKEN = None


def login():
    global TOKEN
    payload = {
        "source": "show",
        "username": "auto_test_jxm",
        "password": "auto_test_jxm123",
        "permission": "on",
    }
    headers = {
        "priority": "u=1, i",
        "content-type": "application/json",
    }
    response = requests.post(LOGIN_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    TOKEN = data.get("data", {}).get("token")
    if not TOKEN:
        raise RuntimeError(f"登录失败，未获取到 token: {response.text[:200]}")
    print(f"登录成功，token: {TOKEN[:20]}...")


def get_headers():
    if not TOKEN:
        login()
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Origin": "https://metahuman-prod.wair.ac.cn",
        "Referer": "https://metahuman-prod.wair.ac.cn/create/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
    }

def get_human_list(page=1, page_size=100, org=2):
    payload = {"page": page, "page_size": page_size, "org": org}
    response = requests.post(API_URL, headers=get_headers(), json=payload)
    return response.json()

def delete_human(human_id):
    payload = {"human_id": human_id}
    response = requests.post(DELETE_URL, headers=get_headers(), json=payload)
    return response.json()

def cleanup_old_humans(days=7):
    cutoff_date = datetime.now() - timedelta(days=days)
    page = 1
    total_deleted = 0

    while True:
        result = get_human_list(page=page)
        human_list = result.get("data", {}).get("list", [])

        if not human_list:
            break

        for human in human_list:
            update_time_val = human.get("update_time")
            if not update_time_val:
                continue

            if isinstance(update_time_val, int):
                update_time = datetime.fromtimestamp(update_time_val)
            else:
                update_time = datetime.fromisoformat(update_time_val.replace("Z", "+00:00"))
                update_time = update_time.replace(tzinfo=None)

            if update_time < cutoff_date:
                human_id = human.get("id")
                print(f"Deleting human_id: {human_id}, update_time: {update_time_val}")
                delete_result = delete_human(human_id)
                print(f"Delete result: {delete_result}")
                total_deleted += 1

        page += 1

    print(f"Total humans deleted: {total_deleted}")
    return total_deleted

def get_voice_list(page=1, page_size=100, org=2):
    payload = {"page": page, "page_size": page_size, "org": org}
    response = requests.post(VOICE_LIST_URL, headers=get_headers(), json=payload, timeout=30)
    return response.json()

def delete_voice(voice_id, clone=False):
    payload = {"voice_id": voice_id, "clone": clone}
    response = requests.post(VOICE_DELETE_URL, headers=get_headers(), json=payload)
    return response.json()

def cleanup_old_voices(days=7, max_pages=50):
    cutoff_date = datetime.now() - timedelta(days=days)
    page = 1
    total_deleted = 0

    while page <= max_pages:
        print(f"Fetching voice page {page}...")
        result = get_voice_list(page=page)
        voice_list = result.get("data", {}).get("list", [])

        if not voice_list:
            print("No more voice records, stopping.")
            break

        for voice in voice_list:
            update_time_val = voice.get("update_time")
            if not update_time_val:
                continue

            if isinstance(update_time_val, int):
                update_time = datetime.fromtimestamp(update_time_val)
            else:
                update_time = datetime.fromisoformat(update_time_val.replace("Z", "+00:00"))
                update_time = update_time.replace(tzinfo=None)

            if update_time < cutoff_date:
                voice_id = voice.get("id")
                print(f"Deleting voice_id: {voice_id}, update_time: {update_time_val}")
                delete_result = delete_voice(voice_id)
                print(f"Delete result: {delete_result}")
                total_deleted += 1

        page += 1

    print(f"Total voices deleted: {total_deleted}")
    return total_deleted

def get_ai_list(page=1, page_size=100, server_type="img", content=""):
    payload = {"page": page, "page_size": page_size, "server_type": server_type, "content": content}
    response = requests.post(AI_LIST_URL, headers=get_headers(), json=payload)
    return response.json()

def delete_ai(asset_id):
    payload = {"id": asset_id}
    response = requests.post(AI_DELETE_URL, headers=get_headers(), json=payload)
    return response.json()

def cleanup_old_ai(days=7):
    cutoff_date = datetime.now() - timedelta(days=days)
    page = 1
    total_deleted = 0

    while True:
        result = get_ai_list(page=page)
        ai_list = result.get("data", {}).get("list", [])

        if not ai_list:
            break

        for ai in ai_list:
            update_time_val = ai.get("update_time")
            if not update_time_val:
                continue

            if isinstance(update_time_val, int):
                update_time = datetime.fromtimestamp(update_time_val)
            else:
                update_time = datetime.fromisoformat(update_time_val.replace("Z", "+00:00"))
                update_time = update_time.replace(tzinfo=None)

            if update_time < cutoff_date:
                asset_id = ai.get("id")
                print(f"Deleting ai_id: {asset_id}, update_time: {update_time_val}")
                delete_result = delete_ai(asset_id)
                print(f"Delete result: {delete_result}")
                total_deleted += 1

        page += 1

    print(f"Total ai assets deleted: {total_deleted}")
    return total_deleted

if __name__ == "__main__":
    cleanup_old_humans(days=7)
    cleanup_old_voices(days=7)
    cleanup_old_ai(days=7)