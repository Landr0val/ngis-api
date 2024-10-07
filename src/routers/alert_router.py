from fastapi import FastAPI, Body, APIRouter, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.reads_model import Read
from src.models.alert_model import Alert
from src.controllers.alert_controller import AlertController
from pydantic import BaseModel

alert_controller = AlertController()

alert_router = APIRouter()

@alert_router.post("/createAlert")
async def save_alert(alert: Alert):
    response = alert_controller.create_alert(alert)
    return response

class UserRequest(BaseModel):
    user_id: int

@alert_router.get("/get_alert_config/{user_id}")
def get_alert_config_endpoint():
    response = alert_controller.get_alert_config(user_id)
    return response