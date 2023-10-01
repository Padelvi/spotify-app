from pydantic import BaseModel
from typing import Literal

class JustID(BaseModel):
    id: str

class SetRepeat(BaseModel):
    repeat: Literal["track", "context", "off"]
