import requests

# pylint: disable=duplicate-code

url = "http://192.168.1.1/osc/commands/execute"
headers = {"Content-Type": "application/json;charset=utf-8"}

# 確認したいオプションを parameters に必ず入れる
payload = {
    "name": "camera.getOptions",
    "parameters": {
        "optionNames": ["iso", "shutterSpeed", "aperture", "_colorTemperature"]
    },
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json())
