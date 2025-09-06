"""Theta Web APIを利用した関数"""

from enum import Enum
import requests


class _ThetaConstans(str, Enum):
    THETA_IP = "192.168.1.1"
    EXECUTE_URL = f"http://{THETA_IP}/osc/commands/execute"
    STATUS_URL = f"http://{THETA_IP}/osc/commands/status"
    HEADERS = {"Content-Type": "application/json;charset=utf-8"}


class _Name(str, Enum):
    SET_OPTIONS = "camera.setOptions"
    GET_OPTIONS = "camera.getOptions"
    TAKE_PICTURE = "camera.takePicture"


class _Parameter(str, Enum):
    OPTIONS = "options"
    OPTION_NAMES = "optionNames"

class Options(str, Enum):
    CAPTURE_MODE = "captureMode"
    EXPOSURE_PROGRAM = "exposureProgram"
    SLEEP_DELAY = "sleepDelay"
    ISO = "iso"
    SHUTTER_SPEED = "shutterSpeed"
    WHITE_BALANCE = "whiteBalance"
    COLOR_TEMPERATURE = "_colorTemperature" #Theta API only
    SHUTTER_VOLUME = "_shutterVolume" #Theta API only

class CameraError(Exception):   
    """全てのカメラ関連エラーの基底クラス"""

class CameraTimeout(CameraError):
    """カメラ操作のタイムアウトした場合の例外"""

class CameraInternalError(CameraError):
    """Open Spherical Camera APIがエラーを返した場合の例外"""

    def __init__(self, code:str, message:str, response_json:dict[str,any]=None):
        """
        Args:
            code: APIが出力するエラーコード（e.g., "invalidParameterValue"）
            message: エラーメッセージ
            response_json: レスポンスの情報が入ったJSONデータ(Optional)
        """
        self.code = code
        self.message = message
        self.response_json = response_json
        super().__init__(f"OSC API Error [{code}]: {message}")


def _create_payload(name: str, parameters: dict[str, any] | None = None) -> dict[str, any]:
    if (dict is None):
        return {"name":name}
    return {"name": name, "parameters": parameters}

def set_options(parameters:dict[str, any], timeout:float = 10.0) -> dict[str, any]:
    """カメラにオプションを設定します。

    Args:
        parameters (dict[str, any]): Theta Web API v2.1に掲載のオプション名と設定値
        timeout (float, optional): POSTリクエストのタイムアウト時間. Defaults to 10.0.

    Raises:
        CameraInternalError: Theta内部でエラーが発生
        CameraTimeout: リクエストのタイムアウト

    Returns:
        dict[str, any]: Thetaからのレスポンス
    """
    payload = _create_payload(
        _Name.SET_OPTIONS,
        {_Parameter.OPTIONS: parameters},
    )

    try:
        response = requests.post(
            url=_ThetaConstans.EXECUTE_URL,
            json=payload,
            headers=_ThetaConstans.HEADERS,
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            err = data["error"]
            raise CameraInternalError(err.get("code"), err.get("message"), data)
        return response.json
    except requests.exceptions.Timeout as e:
        raise CameraTimeout("タイムアウトしました") from e

def get_options(option_names:set[str], timeout:float = 10.0) -> dict[str, any]:
    """カメラの状態を確認します。

    Args:
        option_names (set[str]): Theta Web API v2.1に掲載の確認したいオプション名
        timeout (float, optional): POSTリクエストのタイムアウト時間. Defaults to 10.0.

    Raises:
        CameraInternalError: Theta内部でエラーが発生
        CameraTimeout: リクエストのタイムアウト

    Returns:
        dict[str, any]: Thetaからのレスポンス
    """
    payload = _create_payload(
        _Name.GET_OPTIONS,
        {_Parameter.OPTION_NAMES:option_names}
        )

    try:
        response = requests.post(
            url=_ThetaConstans.EXECUTE_URL,
            json=payload,
            headers=_ThetaConstans.HEADERS,
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            err = data["error"]
            raise CameraInternalError(err.get("code"), err.get("message"), data)
        return response.json
    except requests.exceptions.Timeout as e:
        raise CameraTimeout("タイムアウトしました") from e

def take_picture(timeout:float=10.0) -> dict[str, any]:
    """カメラで撮影します。

    Args:
        timeout (float, optional): POSTリクエストのタイムアウト時間. Defaults to 10.0.

    Raises:
        CameraInternalError: Theta内部でエラーが発生
        CameraTimeout: リクエストのタイムアウト

    Returns:
        dict[str, any]: Thetaからのレスポンス
    """
    payload = _create_payload(_Name.TAKE_PICTURE)

    try:
        response = requests.post(
            _ThetaConstans.EXECUTE_URL, 
            json=payload, 
            headers=_ThetaConstans.HEADERS, 
            timeout=timeout
            )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            err = data["error"]
            raise CameraInternalError(err.get("code"), err.get("message"), data)
        return response.json()
    except requests.exceptions.Timeout as e:
        raise CameraTimeout("タイムアウトしました") from e
