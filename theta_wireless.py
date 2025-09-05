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

class ThetaWirelessResponse(dict[str,str], Enum):
    TIMEOUT = {"error":"time_out"}


def _create_payload(name: str, parameters: dict[str, any] | None = None) -> dict[str, any]:
    if (dict is None):
        return {"name":name}
    else:
        return {"name": name, "parameters": parameters}


def set_options(parameters:dict[str, any]) -> dict[str, any]:
    """
    Thetaへオプションの設定を行う
    """
    payload = _create_payload(
        Name.SET_OPTIONS,
        {Parameter.OPTIONS: parameters},
    )

    try:
        response = requests.post(
            url=ThetaConstans.EXECUTE_URL,
            json=payload,
            headers=ThetaConstans.HEADERS,
            timeout=10,
        )
        return response.json
    except requests.exceptions.Timeout:
        return ThetaWirelessResponse.TIMEOUT

def get_options(option_names:set[str]) -> dict[str, any]:
    """
    Thetaに設定したオプションの情報を取得する
    """
    payload = _create_payload(
        Name.GET_OPTIONS,
        {Parameter.OPTION_NAMES:option_names}
        )
    
    try:
        response = requests.post(
            url=ThetaConstans.EXECUTE_URL,
            json=payload,
            headers=ThetaConstans.HEADERS,
            timeout=10
        )
        return response.json
    except requests.exceptions.Timeout:
        return ThetaWirelessResponse.TIMEOUT
    

def take_picture() -> dict[str, any]:
    """
    Theta Web APIを用いて撮影
    """
    payload = _create_payload(Name.TAKE_PICTURE)
    response = requests.post(
        ThetaConstans.EXECUTE_URL, 
        json=payload, 
        headers=ThetaConstans.HEADERS, 
        timeout=10
        )
    response.raise_for_status()
    return response.json()
