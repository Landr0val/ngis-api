from pydantic import BaseModel

class AlertConfig(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    user_id: int
    temperature_threshold_id: int
    air_humidity_threshold_id: int
    soil_humidity_threshold_id: int
class Alert(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    alert_config_id: int