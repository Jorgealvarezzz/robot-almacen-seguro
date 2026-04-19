"""Entry point FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import init_db
from app.mqtt_subscriber import start_subscriber
from app.routes import router

app = FastAPI(title="Robot Almacen Seguro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    start_subscriber()


app.include_router(router)
