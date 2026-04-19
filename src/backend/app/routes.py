"""Rutas de la API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import authenticate, create_token, require_admin, require_user
from app.models import (
    ComandoORM,
    ComandoOut,
    ComandoRequest,
    EventoORM,
    EventoOut,
    LoginRequest,
    SessionLocal,
    TelemetryORM,
    TelemetryOut,
    TokenResponse,
)
from app.mqtt_subscriber import publish_command

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/health")
def health():
    return {"status": "ok"}


@router.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = authenticate(body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    token = create_token(user["username"], user["role"])
    return TokenResponse(access_token=token, role=user["role"])


@router.get("/api/telemetry", response_model=list[TelemetryOut])
def get_telemetry(
    limit: int = Query(50, ge=1, le=500),
    robot_id: str | None = None,
    claims: dict = Depends(require_user),
    db: Session = Depends(get_db),
):
    q = db.query(TelemetryORM)
    if robot_id:
        q = q.filter(TelemetryORM.robot_id == robot_id)
    rows = q.order_by(TelemetryORM.id.desc()).limit(limit).all()
    return rows


@router.get("/api/telemetry/last")
def get_last_telemetry(
    claims: dict = Depends(require_user),
    db: Session = Depends(get_db),
):
    row = db.query(TelemetryORM).order_by(TelemetryORM.id.desc()).first()
    if row is None:
        return None
    return TelemetryOut.model_validate(row)


@router.get("/api/eventos", response_model=list[EventoOut])
def get_eventos(
    limit: int = Query(50, ge=1, le=500),
    claims: dict = Depends(require_user),
    db: Session = Depends(get_db),
):
    rows = db.query(EventoORM).order_by(EventoORM.id.desc()).limit(limit).all()
    return rows


@router.post("/api/comandos", response_model=ComandoOut, status_code=202)
def post_comando(
    body: ComandoRequest,
    claims: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    try:
        publish_command(body.robot_id, body.cmd)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Broker no disponible: {e}")

    row = ComandoORM(
        robot_id=body.robot_id,
        cmd=body.cmd,
        usuario=claims.get("sub", "unknown"),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/api/comandos", response_model=list[ComandoOut])
def get_comandos(
    limit: int = Query(50, ge=1, le=500),
    claims: dict = Depends(require_user),
    db: Session = Depends(get_db),
):
    rows = db.query(ComandoORM).order_by(ComandoORM.id.desc()).limit(limit).all()
    return rows


@router.get("/api/me")
def me(claims: dict = Depends(require_user)):
    return {"username": claims.get("sub"), "role": claims.get("role")}
