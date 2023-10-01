import os
from dotenv import load_dotenv

load_dotenv()

fields = [
    "CLIENT_ID",
    "CLIENT_SECRET",
    "REDIRECT_URI",
]

environ = {key: value for key, value in dict(os.environ).items() if key in fields}
