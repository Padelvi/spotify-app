import requests
import random
from ..env import environ
from ..backend import get_token_headers
from ..utils import add_content_type_to_headers, verify_request

headers = get_token_headers()

def add_items(index: str, tracks: list):
    url = "{}/playlists/{}/tracks".format(environ["BASE_URL"], index)

    uris = list(map(lambda obj: obj["uri"], tracks))
    random.shuffle(uris)

    post_req = requests.post(url, headers=headers, json = {
        "uris": uris
    })

    verify_request(post_req, "Post request", 201)
