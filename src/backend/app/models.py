"""Modelos Pydantic (validacion) y SQLAlchemy (persistencia)."""
import os
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.getenv("DB_PATH", "/data/robot.db")
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TelemetryORM(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String(32), index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    x = Column(Float)
    y = Column(Float)
    battery = Column(Float)
    status = Column(String(32))
    obstacle = Column(Boolean, default=False)


class EventoORM(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String(32), index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    tipo = Column(String(64))
    payload = Column(String(1024))


class ComandoORM(Base):
    __tablename__ = "comandos"
    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String(32), index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    cmd = Column(String(64))
    usuario = Column(String(64))


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=3, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class TelemetryOut(BaseModel):
    id: int
    robot_id: str
    ts: datetime
    x: float
    y: float
    battery: float
    status: str
    obstacle: bool

    class Config:
        from_attributes = True


class EventoOut(BaseModel):
    id: int
    robot_id: str
    ts: datetime
    tipo: str
    payload: str

    class Config:
        from_attributes = True


class ComandoRequest(BaseModel):
    robot_id: str = Field(..., min_length=2, max_length=32, pattern=r"^[a-zA-Z0-9\-_]+$")
    cmd: str = Field(..., pattern=r"^(STOP|MOVE|CHARGE)$")


class ComandoOut(BaseModel):
    id: int
    robot_id: str
    ts: datetime
    cmd: str
    usuario: str

    class Config:
        from_attributes = True
