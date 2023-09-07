import requests
from ..env import environ
from ..utils import make_request

scope = ["user-read-playback-state",]

def get_playback():
    url = "{}/me/player".format(environ["BASE_URL"])
    req = make_request(requests.get, url, "Get playback", scope)
    return req.json()

if __name__ == "__main__":
    print(get_playback())
