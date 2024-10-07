from pydantic import BaseModel

class Alert(BaseModel):
    temperature: float
    air_humidity: float
    soil_humidity: float
    user_id: int