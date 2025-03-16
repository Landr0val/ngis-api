from pydantic import BaseModel
from typing import Optional

class TokenResponse(BaseModel):
    access_token: str

class UserRequest(BaseModel):
    user_id: int