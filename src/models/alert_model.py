from pydantic import BaseModel

class AlertConfig(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    user_id: int

class Alert(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    alert_config_id: int