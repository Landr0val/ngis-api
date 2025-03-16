from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.controllers.login_crontroller import LoginController
from src.models.users_model import TokenResponse

auth_router = APIRouter()
login_controller = LoginController()

@auth_router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return login_controller.login(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
