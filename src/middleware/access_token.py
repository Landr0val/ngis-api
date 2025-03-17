import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE= int(os.getenv("ACCESS_TOKEN_EXPIRE"))

def create_access_token(user_id: int, username: str, email: str, rol_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    payload = {
        "sub": str(user_id),
        "username": username,
        "email": email,
        "rol_id": rol_id,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token