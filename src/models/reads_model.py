from pydantic import BaseModel

# class Read(BaseModel):
#     humidity: str
#     temperature_c: str
#     temperature_f: str
#     temperature_k: str

class Read(BaseModel):
    device_type: int
    value: float
    id_user: int