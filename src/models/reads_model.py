from pydantic import BaseModel
class Read(BaseModel):
    device_type: int
    value: float
    id_user: int