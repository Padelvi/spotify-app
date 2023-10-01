import requests
import random
from ..utils import (
    extract_sp_link,
    make_request,
)

scope = ["playlist-read-private", "playlist-modify-private", "playlist-modify-public"]

def group_tracks(tracks):
    total = len(tracks)
    segments = (total // 100) + 1
    final = []
    for iter in tuple(range(segments)):
        iter += 1
        iter *= 100
        segment = tracks[(iter-100):iter]
        final.append(segment)
    return final

def collect_playlist(endpoint: str, offset: int):
    get_req = make_request(
        requests.get,
        endpoint,
        "Get request",
        scope,
        params={
            "fields": "items",
            "limit": 50,
            "offset": offset,
    })

    get_json = get_req.json()

    return list(map(
        lambda obj: {"uri": obj["track"]["uri"]},
        get_json["items"]
    ))

def clear_tracks(endpoint: str, total_tracks: list):
    for tracks in total_tracks:
        delete_req = make_request(
            requests.delete,
            endpoint,
            "Delete request",
            scope,
            json={
                "tracks": tracks
        })

def add_items_randomly(endpoint: str, tracks: list):
    to_shuffle = []

    for segment in tracks:
        for item in segment:
            to_shuffle.append(item)

    random.shuffle(to_shuffle)

    total_uris = list(map(lambda obj: obj["uri"], to_shuffle))
    grouped_uris = group_tracks(total_uris)

    for uris in grouped_uris:
        post_req = make_request(
            requests.post,
            endpoint,
            "Post request",
            scope,
            json={
                "uris": uris
        })

def shuffle_playlist(index:str):
    endpoint = "/playlists/{}/tracks".format(index)

    total_req = make_request(
        requests.get,
        endpoint,
        "First request",
        scope,
        params={
            "fields": "total",
    })

    total = total_req.json()["total"]
    repeat = total // 50 + 1
    offset_l = [iter * 50 for iter in tuple(range(repeat))]
    tracks = []

    for offset in offset_l:
        tracks_now = collect_playlist(endpoint, offset)
        for track in tracks_now:
            tracks.append(track)

    grouped_tracks = group_tracks(tracks)

    clear_tracks(endpoint, grouped_tracks)

    add_items_randomly(endpoint, grouped_tracks)

if __name__ == "__main__":
    index = extract_sp_link(
        input("Playlist link: "),
        "playlist"
    )
    shuffle_playlist(index)
