import requests
from ..utils import verify_request
from ..backend import get_token_headers

headers = get_token_headers()

def clear_tracks(url: str, total_tracks: list):
    for tracks in total_tracks:
        delete_req = requests.delete(url, headers=headers, json={
            "tracks": tracks
        })

        verify_request(delete_req, "Delete request", 200)
