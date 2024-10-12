from pydantic import BaseModel
from typing import Optional

class AlertConfig(BaseModel):
    user_id: int
    temperature: Optional[float] = None
    air_humidity: Optional[float] = None
    soil_humidity: Optional[float] = None
    temperature_threshold_id: Optional[int] = None
    air_humidity_threshold_id: Optional[int] = None
    soil_humidity_threshold_id: Optional[int] = None
class Alert(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    alert_config_id: int