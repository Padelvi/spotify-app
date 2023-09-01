import os
from dotenv import load_dotenv

load_dotenv()

keys = [
    "CLIENT_ID",
    "CLIENT_SECRET",
    "REDIRECT_URI",
    "BASE_URL",
    "AUTH_URL",
    "TOKEN_URL",
    "TOKEN_SCOPE",
    "API_PORT",
]

environ = {key: value for key, value in dict(os.environ).items() if key in keys}
