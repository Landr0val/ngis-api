from fastapi import FastAPI, Body, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect
from src.models.reads_model import Read
from src.controllers.reads_controller import ReadsController

reads_controller = ReadsController()


reads_router = APIRouter()


@reads_router.post("/reads")
async def save_read(read: Read):
    response = reads_controller.create_read(read)
    return response


@reads_router.get("/get_reads")
async def get_reads():
    response = reads_controller.get_reads()
    return response

