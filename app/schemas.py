from pydantic import BaseModel
from typing import List

class AuthForm(BaseModel):
    scope: List[str]
    recharge_scope: bool
