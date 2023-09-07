import requests
import webbrowser
import random
import string
import base64
from typing import Callable, List
from .env import environ
from json import JSONDecodeError
from .token import(
    store_state,
    store_tokens,
    get_refresh_token,
    get_state,
    get_token
)

#Get random string used to verify the same user is making authorization steps 1&2
def initialize_state():
    letters = string.ascii_letters
    state = ''.join(random.choice(letters) for _ in range(16))
    store_state(state)

#Compare state values
def invalid_state(state_to_compare):
    return get_state() != state_to_compare

#Get form values required to make authorization step 1 request
def get_auth_params(scope: List[str]):
    return {
        'client_id': environ["CLIENT_ID"],
        'response_type': 'code',
        'redirect_uri': environ["REDIRECT_URI"],
        'state': get_state(),
        'scope': " ".join(scope),
    }

#Get clientID and clientSecret values encrypted, used for step 1 request
def get_encrypted_credentials():
    client_id = environ["CLIENT_ID"]
    client_secret = environ["CLIENT_SECRET"]
    credentials = f'{client_id}:{client_secret}'
    return base64.b64encode(credentials.encode()).decode()

#Get header values for step 1 and 2 request
def get_auth_headers(encoded_credentials):
    return {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

#Get form values required to make authorization step 2 request
def get_token_params(code):
    return {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': environ["REDIRECT_URI"],
    }

#Make the POST request to retrieve and store the tokens in authorization step 2
def request_token(code):
    encoded_credentials = get_encrypted_credentials()
    headers = get_auth_headers(encoded_credentials)
    form_params = get_token_params(code)
    response = requests.post(environ["TOKEN_URL"],
                             headers=headers,
                             data=form_params
    )
    if response.status_code == 200:
        store_tokens(response.json()['access_token'], response.json()['refresh_token'])
    else:
        return response.json()['error']
    
#Get form values required to make a refresh token request    
def get_refresh_token_params():
    return {
        'grant_type': 'refresh_token',
        'refresh_token': get_refresh_token()
    }

def refresh_token():
    if get_refresh_token() is not None:
        refresh_token = get_refresh_token()
        encoded_credentials = get_encrypted_credentials()
        headers = get_auth_headers(encoded_credentials)
        form_params = get_refresh_token_params()
        response = requests.post(environ["TOKEN_URL"],
                                 headers=headers,
                                 data=form_params
        )
        if response.status_code == 200:
            store_tokens(response.json()['access_token'], refresh_token)
            return True
    return False

#Get header values for future Spotify API Requests, using token
def get_token_headers():
    token = get_token()
    if token is not None:
        return {
            'Authorization': f'Bearer {token}',
        }

def extract_sp_link(link: str, verify_type: str):
    segments = link.split("/")
    return segments[-1].split("?")[0], segments[-2] == verify_type

def verify_request(req: requests.Response, desc: str, scope: List[str], recharge: bool):
    print(f"{desc} results:")
    if req.status_code in (401, 403):
        msg = "Re-authenticating... (401)"
        auth = False
        auth_req = requests.post("http://localhost:8000/authorize", json={
            "scope": scope,
            "recharge_scope": recharge
        })
        params = auth_req.json()
        print(params)
        token_req = requests.get(
            environ["AUTH_URL"],
            params=params,
            allow_redirects=True
        )
        if token_req.status_code == 200:
            print(token_req.url)
            try:
                print(token_req.json())
            except JSONDecodeError:
                print("Decoding error")
                webbrowser.open_new_tab(token_req.url)
        else:
            print(f"Error: code {token_req.status_code}")

    elif req.status_code < 400:
        msg = f"No errors. Code {req.status_code}"
        auth = True
    else:
        msg = f"Error: code {req.status_code}"
        auth = True
        print(req.json())
    print(msg + "\n")
    print(auth)
    return auth

def make_request(
    request_method: Callable[..., requests.Response],
    url: str,
    desc: str,
    scope: List[str],
    **req_args
):
    req = request_method(url=url, headers=get_token_headers(), **req_args)
    print(req.json())
    # msg_to_recharge = {}
    # msg_to_recharge[req.json()["msg"]]
    auth = verify_request(req, desc, scope, True)
    if not auth:
        second_req = request_method(url=url, headers=get_token_headers(), **req_args)
        print(second_req.json())
        return second_req
    return req
