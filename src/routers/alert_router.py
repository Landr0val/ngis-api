from fastapi import FastAPI, Body, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.reads_model import Read
from src.controllers.alert_controller import AlertController

alert_controller = AlertController()

alert_router = APIRouter()

@alert_router.post("/createAlert")
async def save_alert(alert: Alert):
    response = alert_controller.create_alert(alert)
    return response

@alert_router.get("/get_alerts")
async def get_reads():
    response = alert_controller.get_alerts()
    return response