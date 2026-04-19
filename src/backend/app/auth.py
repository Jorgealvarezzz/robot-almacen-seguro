"""Autenticacion y autorizacion - JWT HS256."""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "INSECURE_DEFAULT_CHANGE_ME")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_MIN = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

USERS = {
    os.getenv("ADMIN_USER", "admin"): {
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
        "role": "admin",
    },
    os.getenv("OPERADOR_USER", "operador"): {
        "password": os.getenv("OPERADOR_PASSWORD", "op123"),
        "role": "operador",
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=True)


def authenticate(username: str, password: str) -> Optional[dict]:
    user = USERS.get(username)
    if not user:
        return None
    if user["password"] != password:
        return None
    return {"username": username, "role": user["role"]}


def create_token(username: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MIN)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")


def require_user(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_token(token)


def require_admin(token: str = Depends(oauth2_scheme)) -> dict:
    claims = decode_token(token)
    if claims.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere rol admin",
        )
    return claims
