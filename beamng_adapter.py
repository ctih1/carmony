import requests
import json
from audio_manager import CarStatus, Settings

# class BeamngAdapter:
#     def __init__(self):


session = requests.Session()


def get_status(settings: Settings) -> CarStatus:
    res = session.post(
        "http://localhost:29292/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "get_electrics", "arguments": {"vehicle_id": 0}},
        },
    ).json()
    if "electrics requested" in res["result"]["content"][0]["text"]:
        return get_status(settings)

    data = json.loads(res["result"]["content"][0]["text"])

    return CarStatus(
        speed_kmh=data["airspeed"] * 3.6,
        engine_rpm=data["rpm"],
        clutch_depression_percentage=data["clutch"],
        brake_percentage=data["brake"],
        settings=settings,
        throttle_percentage=data["throttle"],
    )
