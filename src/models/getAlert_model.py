from pydantic import BaseModel

class AlertConfig(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float