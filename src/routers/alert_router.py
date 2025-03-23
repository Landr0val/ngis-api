from fastapi import APIRouter, Depends, HTTPException
from src.middleware.auth_wiht_token import get_current_user
from src.models.alert_model import Alert, AlertConfig, AlertConfigUpdate
from src.controllers.alert_controller import AlertController

alert_controller = AlertController()
alert_router = APIRouter()

@alert_router.get("/get_alert_config/{username}")
async def get_alert_config_endpoint(username: str, current_user: dict = Depends(get_current_user)):
    username_token = current_user.get("username")
    if username_token == username:
        return alert_controller.get_alert_config(username)
    raise HTTPException(status_code=401, detail="Unauthorized user")
    
@alert_router.get("/get_alert_config") #public esp32
async def get_all_configs():
    return alert_controller.get_all_configs()

@alert_router.post("/post_alert")#public esp32
async def post_alert(alert: Alert):
    return alert_controller.post_alert(alert)

@alert_router.post("/createAlert")
async def save_alert(alert: AlertConfig, current_user: dict = Depends(get_current_user)):
    return alert_controller.create_alert(alert)
        
@alert_router.put("/updateAlertConfig/{alert_id}")
async def update_alert_config(alert_id: int, alert_update: AlertConfigUpdate, current_user: dict = Depends(get_current_user)):
    return alert_controller.update_alert_config(alert_id, alert_update)
        
@alert_router.delete("/delete_alert_config/{alert_id}", response_model=dict)
async def delete_alert_config(alert_id: int, current_user: dict = Depends(get_current_user)):
    return alert_controller.delete_alert_config(alert_id)