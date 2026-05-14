import requests
from datetime import datetime, timedelta

API_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/human/list"
DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/human/delete"
VOICE_LIST_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/voice/userlist"
VOICE_DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/voice/delete"
AI_LIST_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/ai/list"
AI_DELETE_URL = "https://metahuman-prod.wair.ac.cn/metaman/api/asset/ai/delete"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk0NDIyNDgsImlhdCI6MTc3Njg1MDI0OCwiand0VXNlcklkIjoyMzN9.H7u1O-xWONyE6M1gpQj39f42WeO-CtFqJ27_oO9kMSM"
CASDOOR = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNlcnQtYnVpbHQtaW4iLCJ0eXAiOiJKV1QifQ.eyJhcHBsaWNhdGlvbiI6ImFnZW50IiwiYXVkIjpbIjM3ZThhMzYyMWVmZDliZDU4N2Q4Il0sImRpc3BsYXlOYW1lIjoiYXV0b190ZXN0X2p4bSIsImV4cCI6MTc3OTQ0MjI0OCwiaWF0IjoxNzc2ODUwMjQ4LCJpZCI6IjYxOTUxNzYxNDM1NTgiLCJpc3MiOiJodHRwczovL2F1dGgtaDIwLndhaXIuYWMuY24iLCJqdGkiOiJhZG1pbi8zZWM2M2U3NS1iMjRiLTQwMTEtODE5ZS00NDE1M2FmNjg4ZmUiLCJuYW1lIjoiYXV0b190ZXN0X2p4bSIsIm5iZiI6MTc3Njg1MDI0OCwibm9uY2UiOiIiLCJvd25lciI6ImFnZW50IiwicGFzc3dvcmQiOiIiLCJwaG9uZSI6IiIsInNjb3BlIjoicHJvZmlsZSIsInN1YiI6IjYxOTUxNzYxNDM1NTgiLCJ0YWciOiIiLCJ0b2tlblR5cGUiOiJhY2Nlc3MtdG9rZW4ifQ.SnQXkq-DlXXBusMxOB7dbWmd_o5SVDdXQfYdG1vxpj3DLk6wWIIpV0-r45YvAgrVTnsbFrEICFlTlgM_8u1lENKAIMSsA41LSkOdEAxQL5YuNUKmhnd4JQlu-Ytfs_P2EGhIHHfmhNbvTz-0JSrYafE40fRvLHvkSWCtkFTOBohT0z_WaM_Xo_XRNw8xwD3ygNUD8rADNGf1sKzSwflQkcGVbvfxLhYyG3xcWskcV2zhcealR-XSlIrA5262D5p_jGYkPafVJ_iMfyzHCXqeYHhl2lyoQIsw4S4hrkW684WwDEkhnqnbGTdZqThlnQEviW3QSJpvHN1Xi9wIOvxBVntH05IZ-MHny8bR_RV5cRqHpZnXc2gBCJXyL7stbs5djkziGNpippk3LMWc9_cQekg7IILABvVuBGkYUxTHnpf7DJOPbPItKuAPDUi7uFPeyLn8m5HAMa5PH8Xr35XLY-1Fv85kP62UNQYkINJdThB459k9FjT2K5TGYurgqJYSWTTOT9PfUc_PjDjnIWcKzSYwW6wf1eCfl73pI3Za2gx1YYsPDIKBDwh_YV793qYAMb3g2IXGzLUKHK_l55GSXZAj8q6nBmqlqypVCk6ROgNmMUCoEAJ1z5hjyrJuSXw20m4HDIxZTb20wgq5aYu0Wd9oIbA5XyiHOQwzT6lVuo4"

def get_headers():
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Authorization": f"Bearer {TOKEN}",
        "Casdoor": CASDOOR,
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