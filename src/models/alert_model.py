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
    temp_threshold_id: int
    air_threshold_id: int
    soil_threshold_id: int