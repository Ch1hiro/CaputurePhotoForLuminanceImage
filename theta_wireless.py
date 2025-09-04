"""Theta Web APIを利用した関数"""

from enum import Enum
import requests

class ThetaConstans(str, Enum):
    THETA_IP = "192.168.1.1"
    EXECUTE_URL = f"http://{THETA_IP}/osc/commands/execute"
    STATUS_URL = f"http://{THETA_IP}/osc/commands/status"
    HEADERS = {"Content-Type": "application/json;charset=utf-8"}

class Name(str, Enum):
    SET_OPTIONS = "camera.setOptions"
    GET_OPTIONS = "camera.getOptions"
    TAKE_PICTURE = "camera.takePicture"

class Parameter(str, Enum):
    OPTIONS = "options"
    OPTION_NAMES = "optionNames"


def _create_payload(name: str, parameters: dict[str, any]) -> dict[str, any]:
    return {"name": name, "parameters": parameters}


def camera_init() -> None:
    """
    カメラの初期化を行う関数
    """
    payload = _create_payload(
        Name.SET_OPTIONS,
        {Parameter.OPTIONS: ["captureMode":"image", "exposureProgram":1]}
    )


payload = {
    "name": "camera.setOptions",
    "parameters": {"options": {"captureMode": "image"}},
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json())

payload = {
    "name": "camera.setOptions",
    "parameters": {"options": {"exposureProgram": 1}},
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json())

# 確認したいオプションを parameters に必ず入れる
payload = {
    "name": "camera.getOptions",
    "parameters": {
        "optionNames": ["iso", "shutterSpeed", "aperture", "_colorTemperature"]
    },
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json())
