"""Script for controlling RICOH THETA camera."""

import requests

# pylint: disable=duplicate-code

URL = "http://192.168.1.1/osc/commands/execute"
HEADERS = {"Content-Type": "application/json;charset=utf-8"}

# 確認したいオプションを parameters に必ず入れる
payload = {
    "name": "camera.getOptions",
    "parameters": {
        "optionNames": ["iso", "shutterSpeed", "aperture", "_colorTemperature"]
    },
}

resp = requests.post(URL, json=payload, headers=HEADERS, timeout=10)
print(resp.json())
