from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from typing import Dict, Any

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    print(f"DEBUG: A password recebida é: {password}")
    print(f"DEBUG: O tipo é: {type(password)}")
    print(f"DEBUG: O tamanho é: {len(str(password))}")
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

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.JWTError:
        raise Exception("Token inválido")