import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE","30"))

if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY set for access token generation")
if ALGORITHM is None:
    raise ValueError("No ALGORITHM set for access token generation")
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise ValueError("No ACCESS_TOKEN_EXPIRE_MINUTES set for access token generation")
    

def create_access_token(user_id: int, username: str, email: str, rol_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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