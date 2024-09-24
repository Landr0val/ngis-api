from pydantic import BaseModel
class Read(BaseModel):
    device_id: int
    unit_id: int
    id_user: int
    value: float