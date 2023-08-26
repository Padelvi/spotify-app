import requests
from ..backend import get_token_headers
from ..utils import verify_request

headers = get_token_headers()

def collect_playlist(url: str, offset: int):
    get_req = requests.get(url, headers=headers, params={
        "fields": "items",
        "limit": 50,
        "offset": offset,
    })

    get_json = get_req.json()

    verify_request(get_req, "Get request", 200)

    return list(map(
        lambda obj: {"uri": obj["track"]["uri"]},
        get_json["items"]
    ))
