from fastapi import FastAPI, Body, APIRouter, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.reads_model import Read
from src.models.alert_model import Alert, AlertConfig, AlertConfigUpdate
from src.controllers.alert_controller import AlertController
from pydantic import BaseModel

alert_controller = AlertController()

alert_router = APIRouter()

@alert_router.post("/createAlert")
async def save_alert(alert: AlertConfig):
    response = alert_controller.create_alert(alert)
    return response

class UserRequest(BaseModel):
    user_id: int

@alert_router.get("/get_alert_config/{user_id}")
def get_alert_config_endpoint(user_id):
    response = alert_controller.get_alert_config(user_id)
    return response

@alert_router.get("/get_alert_config")
def get_all_configs():
    response = alert_controller.get_all_configs()
    return response

@alert_router.post("/post_alert")
def post_alert(alert: Alert):
    response = alert_controller.post_alert(alert)
    return response

@alert_router.put("/updateAlertConfig/{alert_id}")
def update_alert_config(alert_id: int, alert_update: AlertConfigUpdate):
    return alert_controller.update_alert_config(alert_id, alert_update)

@alert_router.delete("/delete_alert_config/{alert_id}")
def delete_alert_config(alert_id: int):
    return alert_controller.delete_alert_config(alertid)