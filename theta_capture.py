"""Script for controlling RICOH THETA camera."""

import time
import datetime

import requests

# pylint: disable=duplicate-code

# カメラIP
THETA_IP = "192.168.1.1"
EXECUTE_URL = f"http://{THETA_IP}/osc/commands/execute"
STATUS_URL = f"http://{THETA_IP}/osc/commands/status"

HEADERS = {"Content-Type": "application/json;charset=utf-8"}

# 撮影設定リスト (ISO, shutter_speed, ColorTemperature)
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
                "whiteBalance": "_colorTemperature",
                "colorTemperature": white_balance,
            }
        },
    }
    resp = requests.post(EXECUTE_URL, json=options_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def take_picture():
    """Theta Web APIを用いて撮影"""
    take_command = {"name": "camera.takePicture"}
    resp = requests.post(EXECUTE_URL, json=take_command, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def wait_for_completion(command_id):
    """撮影完了まで処理を停止"""
    while True:
        status_resp = requests.post(
            STATUS_URL, json={"id": command_id}, headers=HEADERS
        )
        status_resp.raise_for_status()
        status = status_resp.json()
        if status.get("state") == "done":
            return status.get("results")
        time.sleep(0.5)


def capture_12():
    """設定リストに従って12枚連続撮影"""
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


def schedule_shoots():
    """午前6時～午後7時まで1時間おきに3回ずつ撮影"""
    while True:
        now = datetime.datetime.now()
        hour = now.hour

        # 午前6時〜午後7時の間だけ実行
        if 6 <= hour <= 19:
            print(f"\n=== {now} に撮影開始 ===")
            for repeat in range(1, 4):  # 3回繰り返す
                print(f"\n--- セット {repeat}/3 ---")
                capture_12()
                time.sleep(5)  # セット間の待機（秒）

            print(f"\n=== {hour}時の撮影完了 ===")

        # 次の「正時」まで待つ
        next_hour = (now + datetime.timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )
        wait_sec = (next_hour - datetime.datetime.now()).total_seconds()
        if wait_sec < 0:
            next_hour = (now + datetime.timedelta(hours=2)).replace(
                minute=0, second=0, microsecond=0
            )
            wait_sec = (next_hour - datetime.datetime.now()).total_seconds()
        print(f"{wait_sec/60:.1f} 分後の {next_hour} に再開します…")
        for sleepCount in range(0, 61):
            print(f"残り{wait_sec * (60 - sleepCount)/60}秒")
            time.sleep(wait_sec / 60)


if __name__ == "__main__":
    schedule_shoots()
