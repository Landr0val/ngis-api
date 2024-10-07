from fastapi import FastAPI, Body, APIRouter, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.reads_model import Read
from src.models.alert_model import Alert
from src.models.getAlert_model import AlertConfig
from src.controllers.alert_controller import AlertController

alert_controller = AlertController()

alert_router = APIRouter()

@alert_router.post("/createAlert")
async def save_alert(alert: Alert):
    response = alert_controller.create_alert(alert)
    return response

@alert_router.get("/get_alert_config")
def get_alert_config_endpoint(request: AlertConfig = Body(...)):
    response = alert_controller.get_alerts(request.user_id)
    return response