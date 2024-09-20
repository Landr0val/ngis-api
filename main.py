from fastapi import FastAPI, Body, HTTPException
from src.routers.reads_router import reads_router
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth_router import auth_router



app = FastAPI()

app.include_router(router=reads_router)
app.include_router(router=auth_router)

origins = [
    #"http://localhost.tiangolo.com",
    #"https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

        