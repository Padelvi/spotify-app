import requests
from .env import environ
from .backend import get_token_headers
from .utils import extract_sp_link, verify_request, group_tracks
from .collect import collect_playlist
from .add import add_items_randomly

headers = get_token_headers()

link = input("Playlist link: ")

index, verify = extract_sp_link(
    link,
    "playlist"
)

assert verify

url = "{}/playlists/{}/tracks".format(environ["BASE_URL"], index)

def clear_tracks(url: str, total_tracks: list):
    for tracks in total_tracks:
        delete_req = requests.delete(url, headers=headers, json={
            "tracks": tracks
        })
        verify_request(delete_req, "Delete request", 200)

total_req = requests.get(url, headers=headers, params={
    "fields": "total",
})

total = total_req.json()["total"]

verify_request(total_req, "First request", 200)

repeat = total // 50 + 1
offset_l = []
tracks = []

for iter in tuple(range(repeat)):
    offset_l.append(iter * 50)

for offset in offset_l:
    tracks_now = collect_playlist(url, offset)
    for track in tracks_now:
        tracks.append(track)

grouped_tracks = group_tracks(tracks)

clear_tracks(url, grouped_tracks)

add_items_randomly(url, grouped_tracks)
