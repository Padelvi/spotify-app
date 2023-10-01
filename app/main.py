from fastapi import FastAPI, Response
from .token import store_token
from .utils import invalid_state
from .actions import playlist, playback
from . import schemas

app = FastAPI()

@app.get("/callback")
def callback(
    access_token: str,
    token_type: str,
    expires_in: int,
    state: str,
    response: Response
):
    if invalid_state(state):
        response.status_code = 403
        return {
            "msg": "Invalid state"
        }
    store_token(access_token)
    response.status_code = 200
    return {
        "access_token": access_token,
        "token_type": token_type,
        "expires_in": expires_in,
        "state": state,
    }

@app.put("/play")
def play(response: Response):
    req = playback.play()
    response.status_code = req.status_code
    return response

@app.put("/pause")
def pause(response: Response):
    req = playback.pause()
    response.status_code = req.status_code
    return response

@app.put("/next")
def next(response: Response):
    req = playback.next()
    response.status_code = req.status_code
    return response

@app.put("/previous")
def previous(response: Response):
    req = playback.previous()
    response.status_code = req.status_code
    return response

@app.put("/shuffle")
def shuffle(sent: schemas.JustID, response: Response):
    playlist.shuffle_playlist(sent.id)
    response.status_code = 204
    return response
