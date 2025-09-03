"""Script for controlling RICOH THETA camera."""

import requests

# pylint: disable=duplicate-code

URL = "http://192.168.1.1/osc/commands/execute"
HEADERS = {"Content-Type": "application/json;charset=utf-8"}

payload = {
    "name": "camera.setOptions",
    "parameters": {"options": {"captureMode": "image"}},
}

resp = requests.post(URL, json=payload, headers=HEADERS, timeout=10)
print(resp.json())

payload = {
    "name": "camera.setOptions",
    "parameters": {"options": {"exposureProgram": 1}},
}

resp = requests.post(URL, json=payload, headers=HEADERS, timeout=10)
print(resp.json())
