from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.config.db_config import get_db_connection
from jose import jwt
import bcrypt
from os import getenv
from typing import Annotated

load_dotenv()

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, username, email FROM public.user WHERE username = %s", (data["username"],))
                user_result = cursor.fetchone()
                if user_result:
                    return {
                        "user_id": user_result[0],
                        "username": user_result[1],
                        "email": user_result[2]
                    }
                else:
                    raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, username, email, password FROM public.user WHERE username = %s", (form_data.username,))
                user_result = cursor.fetchone()
                if not user_result:
                    raise HTTPException(status_code=400, detail="Invalid username or password")
                
                user_id = user_result[0]
                username = user_result[1]
                email = user_result[2]
                stored_password = user_result[3]
                
                password_bytes = form_data.password.encode('utf-8')
                stored_password_bytes = stored_password.encode('utf-8')
                
                if not bcrypt.checkpw(password_bytes, stored_password_bytes):
                    raise HTTPException(status_code=400, detail="Invalid username or password")
                
                token = encode_token({
                    "user_id": user_id,
                    "username": username,
                    "email": email
                })
                return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
