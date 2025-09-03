import time

import requests

# pylint: disable=duplicate-code

# カメラIP
THETA_IP = "192.168.1.1"
EXECUTE_URL = f"http://{THETA_IP}/osc/commands/execute"
STATUS_URL = f"http://{THETA_IP}/osc/commands/status"

HEADERS = {"Content-Type": "application/json;charset=utf-8"}

# 撮影設定リスト (ISO, shutter_speed, f, ColorTemperature)
settings_list = [
    {"iso": 100, "shutter_speed": 0.00004, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.00008, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.0003125, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.000625, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.0025, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.005, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.02, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.04, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.16666666, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.33333333, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 0.625, "white_balance": 5200},
    {"iso": 100, "shutter_speed": 3.2, "white_balance": 5200},
]


def set_options(iso, shutter_speed, white_balance):
    """オプションを設定"""
    options_command = {
        "name": "camera.setOptions",
        "parameters": {
            "options": {
                "iso": iso,
                "shutterSpeed": shutter_speed,
                "_colorTemperature": white_balance,
            }
        },
    }
    resp = requests.post(EXECUTE_URL, json=options_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def take_picture():
    """Take a picture using the Theta API"""
    take_command = {"name": "camera.takePicture"}
    resp = requests.post(EXECUTE_URL, json=take_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def wait_for_completion(command_id):
    """Wait a few seconds to complete"""
    while True:
        status_resp = requests.post(
            STATUS_URL, json={"id": command_id}, headers=HEADERS
        )
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
