import requests
import random
from ..backend import get_token_headers
from ..utils import verify_request, group_tracks

headers = get_token_headers()

def add_items_randomly(url: str, tracks: list):
    to_shuffle = []

    for segment in tracks:
        for item in segment:
            to_shuffle.append(item)

    random.shuffle(to_shuffle)

    total_uris = list(map(lambda obj: obj["uri"], to_shuffle))
    grouped_uris = group_tracks(total_uris)

    for uris in grouped_uris:
        post_req = requests.post(url, headers=headers, json = {
            "uris": uris
        })

        verify_request(post_req, "Post request", 201)
