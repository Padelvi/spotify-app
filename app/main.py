from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from .modules.env import environ
from .modules.backend import (
    get_auth_params,
    initialize_state,
    request_token,
    refresh_token,
    invalid_state
)

app = FastAPI()

@app.get("/callback")
def callback(code: int, state):
    if invalid_state(state):
        raise HTTPException(status_code=403)
    request_token(code)
    return {
        "msg": "Got to callback url"
    }

@app.get("/authorize")
def authorize():
    if refresh_token():
        return {
            "msg": "Got to callback from authorize"
        }
    else:
        initialize_state()
        params = get_auth_params()
        return RedirectResponse(url=environ["AUTH_URL"] +
            '?' +
            '&'.join([f'{k}={v}' for k, v in params.items()])
        )
