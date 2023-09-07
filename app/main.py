from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from .env import environ
from . import schemas
from .utils import (
    get_auth_params,
    initialize_state,
    request_token,
    refresh_token,
    invalid_state
)

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse("http://localhost:8000/docs")

@app.get("/callback")
def callback(code, state):
    if invalid_state(state):
        raise HTTPException(status_code=403)
    request_token(code)
    return {
        "msg": "Got to callback url"
    }

@app.post("/authorize")
def authorize(form: schemas.AuthForm):
    if refresh_token() and not form.recharge_scope:
        return {
            "msg": "Token refreshed"
        }
    else:
        initialize_state()
        return get_auth_params(form.scope)
