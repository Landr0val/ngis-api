# src/middleware/validation.py
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_user_login(form_data: OAuth2PasswordRequestForm):
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)