from pydantic import BaseModel
class Read(BaseModel):
    device_id: int
    unit_id: int
    user_idr: int
    value: float