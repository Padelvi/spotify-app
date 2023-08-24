import requests
from ..env import environ
from ..backend import get_token_headers

url = "{}/search".format(environ["BASE_URL"])

r = requests.get(url, headers=get_token_headers(), params={
    "q": "amaranthe",
    "type": ["artist", "album"],
    "limit": 3
})

if r.status_code == 200:
    print(r.json())
    print(f"Status code: {r.status_code}")
else:
    print(f"Status code: {r.status_code}")
    print(r.json())

