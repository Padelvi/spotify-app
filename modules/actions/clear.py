import requests
from ..env import environ
from ..utils import verify_request
from ..backend import get_token_headers

headers = get_token_headers()

def clear_playlist(index: str, tracks: list):
    url = "{}/playlists/{}/tracks".format(environ["BASE_URL"], index)

    delete_req = requests.delete(url, headers=headers, json={
        "tracks": tracks
    })

    verify_request(delete_req, "Delete request", 200)
