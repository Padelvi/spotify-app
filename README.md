# Spotify Authorization API template

A python example of the authorization flow in Spotify.
This can be used as a template to play around with the APIs.
This is not designed for production as the tokens are stored locally in a json file, and the flask web server is development.

## Requirements

- A spotify [app](https://developer.spotify.com/documentation/web-api/concepts/apps).
  - Client ID and Client Secret from the app.
  - Redirect URI from the app.
- Python

## Adding missing files and contents

- Create a .env file and fill out contents with:

  - `CLIENT_ID`
  - `CLIENT_SECRET`
  - `REDIRECT_URI`
  - `BASE_URL`
  - `AUTH_URL`
  - `TOKEN_URL`
  - `TOKEN_SCOPE`
  - `FLASK_PORT`

- Create an empty config.json file

  - This will store the token values.
  - This file is included in the git ignore.

## Setup

- Create virtual python environment

  - `python3 -m venv venv`

- Enter virtual environment

  - `source venv/bin/activate`

- Install dependencies

  - `pip install -r requirements.txt`
  - Any future dependencies, place in this file.

- Running tests

  - `pytest`

- Running application
  - `python app.py`
  - Navigate to `localhost:8080` or wherever you choose to run in `app.py` to view.
