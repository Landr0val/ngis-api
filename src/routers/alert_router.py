from fastapi import FastAPI, Body, APIRouter, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.reads_model import Read
from src.models.alert_model import Alert
from src.controllers.alert_controller import AlertController

alert_controller = AlertController()

alert_router = APIRouter()

@alert_router.post("/createAlert")
async def save_alert(alert: Alert):
    response = alert_controller.create_alert(alert)
    return response

@alert_router.get("/get_alert_config")
async def get_alert_config(user_id: int = Query(..., description="ID del usuario para obtener la configuración de alertas")):
    response = alert_controller.get_alerts()
    return response