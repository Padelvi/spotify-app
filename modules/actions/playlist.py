import requests
from ..env import environ
from ..backend import get_token_headers

playlist = "0ksHbUW5uB9qJepdHDnBPN"
url = "{}/playlists/{}".format(environ["BASE_URL"], playlist)

# r = requests.put(url, headers=get_token_headers(), data={
#     "name": "Just experimenting",
#     "public": False
# })

r = requests.get(url, headers=get_token_headers())

if r.status_code == 200:
    print(r.json())
    print(f"Status code: {r.status_code}")
else:
    print(f"Status code: {r.status_code}")
    print(r.json())

