import requests

# pylint: disable=duplicate-code

url = "http://192.168.1.1/osc/commands/execute"
headers = {"Content-Type": "application/json;charset=utf-8"}

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
