import requests
import time

# カメラIP
THETA_IP = "192.168.1.1"
EXECUTE_URL = f"http://{THETA_IP}/osc/commands/execute"
STATUS_URL = f"http://{THETA_IP}/osc/commands/status"

HEADERS = {
    "Content-Type": "application/json;charset=utf-8"
}

# 撮影設定リスト (ISO, ShutterSpeed, f, ColorTemperature)
settings_list = [
    {"iso": 100, "shutterSpeed": 0.00004, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.00008, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.0003125, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.000625, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.0025, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.005, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.02, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.04, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.16666666, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.33333333, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 0.625, "whiteBalance": 5200},
    {"iso": 100, "shutterSpeed": 3.2, "whiteBalance": 5200},
]

def set_options(iso, shutterSpeed, whiteBalance):
    options_command = {
        "name": "camera.setOptions",
        "parameters": {
            "options": {
                "iso": iso,
                "shutterSpeed": shutterSpeed,
                "_colorTemperature": whiteBalance
            }
        }
    }
    resp = requests.post(EXECUTE_URL, json=options_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def take_picture():
    take_command = {"name": "camera.takePicture"}
    resp = requests.post(EXECUTE_URL, json=take_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def wait_for_completion(command_id):
    while True:
        status_resp = requests.post(STATUS_URL, json={"id": command_id}, headers=HEADERS)
        status_resp.raise_for_status()
        status = status_resp.json()
        if status.get("state") == "done":
            return status.get("results")
        time.sleep(0.5)

# 連続撮影
for idx, s in enumerate(settings_list, start=1):
    print(f"\n=== 撮影 {idx}/12 ===")
    set_options(**s)
    print("設定完了:", s)
    
    result = take_picture()
    print("撮影コマンド送信:", result)
    
    if "id" in result:
        pic_result = wait_for_completion(result["id"])
        print("撮影完了:", pic_result)
    else:
        print("即時撮影結果:", result)
