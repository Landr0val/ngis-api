from fastapi import Depends, APIRouter, HTTPException
from src.middleware.auth_wiht_token import get_current_user
from src.models.reads_model import Read
from src.controllers.reads_controller import ReadsController

reads_controller = ReadsController()
reads_router = APIRouter()

@reads_router.post("/reads")
async def save_read(read: Read):
    response = reads_controller.create_read(read)
    return response

@reads_router.get("/get_read/{username}")
async def get_read_user(username: str, current_user: dict = Depends(get_current_user)):
    user_id_from_token = current_user.get("username")
    if user_id_from_token == username:
        return reads_controller.get_read(username)
    
    raise HTTPException(status_code=401, detail="Unauthorized user")

@reads_router.get("/get_reads")
async def get_reads(current_user: dict = Depends(get_current_user)):
    response = reads_controller.get_reads()
    return response

@reads_router.get("/get_last_read")
async def get_last_read(current_user: dict = Depends(get_current_user)):
    response = reads_controller.get_last_read()
    return response