import requests
from ..env import environ
from ..backend import get_token_headers
from ..utils import extract_sp_link, add_content_type_to_headers, verify_request
from .clear import clear_playlist
from .collect import collect_playlist
from .add import add_items

headers = add_content_type_to_headers(get_token_headers())

index, verify = extract_sp_link(
    "https://open.spotify.com/playlist/783nz67tWQm7qBKHSgzWgK",
    "playlist"
)

assert verify

url = "{}/playlists/{}/tracks".format(environ["BASE_URL"], index)

total_req = requests.get(url, headers=headers, params={
    "fields": "total",
})

total = total_req.json()["total"]

verify_request(total_req, "First request", 200)

tracks = collect_playlist(index)

clear_playlist(index, tracks)

input("Pause before POST")

add_items(index, tracks)
