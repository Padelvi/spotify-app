import requests
import webbrowser as wb
from string import ascii_letters
from random import choice
from typing import Callable, List
from .env import environ
from .token import get_token, get_state, store_state

def initialize_state():
    state = ''.join((choice(ascii_letters) for _ in range(16)))
    store_state(state)

def invalid_state(state_to_compare):
    return get_state() != state_to_compare

def get_token_params(scope: List[str]):
    return {
        "client_id": environ["CLIENT_ID"],
        "response_type": "token",
        "redirect_uri": environ["REDIRECT_URI"],
        "state": get_state(),
        "scope": " ".join(scope)
    }

def request_token(scope: List[str]):
    url = "{base_url}?{params}".format(
        base_url="https://accounts.spotify.com/authorize",
        params="&".join(f"{k}={v}" for (k, v) in get_token_params(scope).items())
    )
    wb.open_new_tab(url)
    
def get_request_headers():
    return {
        'Authorization': f'Bearer {get_token()}',
    }

def extract_sp_link(link: str, verify_type: str):
    segments = link.split("/")
    assert segments[-2] == verify_type
    return segments[-1].split("?")[0]

def verify_request(req: requests.Response, desc: str):
    print(f"{desc} results:")
    if req.status_code in (401, 403):
        msg = f"Re-authenticating... ({req.status_code})"
        auth = False
    elif req.status_code < 400:
        msg = f"No errors. Code {req.status_code}"
        auth = True
    else:
        msg = f"Error: code {req.status_code}"
        auth = True
        print(req.json())
    print(msg + "\n")
    return auth

def make_request(
    request_method: Callable[..., requests.Response],
    endpoint: str,
    desc: str,
    scope: List[str],
    **req_args
):
    url = "https://api.spotify.com/v1" + endpoint
    req = request_method(
        url=url,
        headers=get_request_headers(),
        **req_args
    )
    if not verify_request(req, desc):
        initialize_state()
        request_token(scope)
        input("Waiting for token storing")
        second_req = request_method(
            url=url,
            headers=get_request_headers(),
            **req_args
        )
        return second_req
    return req
