from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from typing import Dict, Any

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: str, 
        expires_delta: timedelta | None = None,
        additional_payload: Dict[str, Any] | None = None
):

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": subject,
        "exp": expire
    }

    if additional_payload:
        payload.update(additional_payload)
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token( subject: dict, expires_delta: timedelta | None = None):
    
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    payload = {"sub":  subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_tokens(subject: dict, expires_delta: timedelta | None = None,additional_payload: Dict[str, Any] | None = None):

    return create_access_token(subject, expires_delta, additional_payload), create_refresh_token(subject, expires_delta)