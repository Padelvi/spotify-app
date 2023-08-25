import requests
import random
import string
import base64
from .env import environ
from .token import(
    store_state, store_tokens, get_refresh_token, get_state, get_token
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
def get_auth_params():
    return {
        'client_id': environ["CLIENT_ID"],
        'response_type': 'code',
        'redirect_uri': environ["REDIRECT_URI"],
        'state': get_state(),
        'scope': environ['TOKEN_SCOPE'],
        'show_dialog': 'true'
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
    response = requests.post('https://accounts.spotify.com/api/token',
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
        response = requests.post('https://accounts.spotify.com/api/token',
                                 headers=headers,
                                 data=form_params
                                 )
        if response.status_code == 200:
            store_tokens(response.json()['access_token'], refresh_token)
            return True
    return False

#Get header values for future Spotify API Requests, using token
def get_token_headers():
    return {
        'Authorization': f'Bearer {get_token()}',
    }
