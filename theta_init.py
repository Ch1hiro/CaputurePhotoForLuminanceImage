"""Thetaカメラを初期化します"""

import theta_wireless
from theta_wireless import Options

try:
    theta_wireless.set_options(
        {
            Options.CAPTURE_MODE:"image",
            Options.EXPOSURE_PROGRAM:1,
            Options.SLEEP_DELAY:65535,
            Options.SHUTTER_VOLUME:0
        }
    )
    response = theta_wireless.get_options(
        {
            Options.CAPTURE_MODE,
            Options.EXPOSURE_PROGRAM,
            Options.SLEEP_DELAY,
            Options.SHUTTER_VOLUME
        }
    )
    print(response)

except theta_wireless.CameraInternalError as e:
    print(f"Caught OSC API error: {e.code} -> {e.message}")

except theta_wireless.CameraTimeout as e:
    print("Timeoutしました")

