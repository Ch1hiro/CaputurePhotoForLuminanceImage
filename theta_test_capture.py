"""Script for controlling RICOH THETA camera."""

import time

import theta_wireless as tw
from theta_wireless import Options

# pylint: disable=duplicate-code


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
    tw.set_options(
        {
            Options.ISO:iso,
            Options.SHUTTER_SPEED: shutter_speed,
            Options.WHITE_BALANCE: Options.COLOR_TEMPERATURE,
            Options.COLOR_TEMPERATURE: white_balance
        }
    )
    resp = tw.get_options(
        {
            Options.ISO,
            Options.SHUTTER_SPEED,
            Options.COLOR_TEMPERATURE
        }
    )
    return resp


def wait_for_completion(command_id):
    """Wait a few seconds to complete"""
    while True:
        status = tw.check_status(command_id=command_id)
        if status.get("state") == "done":
            return status.get("results")
        time.sleep(0.5)


# 連続撮影
for idx, s in enumerate(settings_list, start=1):
    print(f"\n=== 撮影 {idx}/12 ===")
    set_options(**s)
    print("設定完了:", s)

    result = tw.take_picture()
    print("撮影コマンド送信:", result)

    if "id" in result:
        pic_result = wait_for_completion(result["id"])
        print("撮影完了:", pic_result)
    else:
        print("即時撮影結果:", result)
