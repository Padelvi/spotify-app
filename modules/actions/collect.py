import requests
from ..env import environ
from ..backend import get_token_headers
from ..utils import add_content_type_to_headers, verify_request

headers = add_content_type_to_headers(get_token_headers())

def collect_playlist(index: str):
    url = "{}/playlists/{}/tracks".format(environ["BASE_URL"], index)

    get_req = requests.get(url, headers=headers, params={
        "fields": "items",
        "limit": 50
    })

    get_json = get_req.json()

    verify_request(get_req, "Get request", 200)

    return list(map(
        lambda obj: {"uri": obj["track"]["uri"]},
        get_json["items"]
    ))
