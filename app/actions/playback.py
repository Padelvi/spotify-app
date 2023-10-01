import requests
from ..utils import make_request

scope = ["user-read-playback-state", "user-modify-playback-state"]

def get_inactive_player():
    endpoint = "/me/player/devices"
    req = make_request(requests.get, endpoint, "Get inactive player", scope)
    devices = tuple(map(
        lambda dev: dev["id"] if not dev["is_active"] else None,
        req.json()["devices"]
    ))
    return devices[0] if devices[0] is not None else devices[1]
    
def transfer_playback(device_id):
    endpoint = "/me/player"
    req = make_request(requests.put, endpoint, "Transfer playback", scope, json={
        "device_ids": [device_id,],
        "play": True
    })

def play():
    return make_request(
        requests.put,
        "/me/player/play",
        "Resume play",
        scope
    )

def pause():
    return make_request(
        requests.put,
        "/me/player/pause",
        "Pause play",
        scope
    )

def next():
    return make_request(
        requests.post,
        "/me/player/next",
        "Skip to next",
        scope
    )

def previous():
    return make_request(
        requests.post,
        "/me/player/previous",
        "Back to previous",
        scope
    )

def set_repeat(state: str):
    return make_request(
        requests.put,
        "/me/player/repeat",
        f"Set repeat to {state}",
        scope
    )

if __name__ == "__main__":
    device = get_inactive_player()
    transfer_playback(device)
