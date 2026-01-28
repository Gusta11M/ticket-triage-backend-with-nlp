from fastapi import HTTPException, status
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password, create_tokens
from app.repositories.user_repository import create_user, get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.core.config import settings
from app.schemas.auth import RefreshTokenRequest, RegisterRequest, LoginRequest


async def register(db:AsyncSession, data : RegisterRequest):

    user = await get_user_by_email(db, data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilizador já existe"
        )
    
    hash = hash_password(data.password)

    data.password = hash

    new_user = await create_user(db, data)

    access_token = create_access_token(subject=str(new_user.id), additional_payload={"role": new_user.role})
    refresh_token = create_refresh_token(subject=str(new_user.id))

    return access_token, refresh_token

async def authenticate_user(db : AsyncSession, data: LoginRequest):

    user = await get_user_by_email(db, data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    access_token = create_access_token(subject=str(user.id), additional_payload={"role": user.role})
    refresh_token = create_refresh_token(subject=str(user.id))

    return access_token, refresh_token

def refresh_tokens(data: RefreshTokenRequest):

    token_str = data.refresh_token 

    try:
        payload = jwt.decode(
            token_str, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")
        
        if isinstance(user_id, dict):
            user_id = user_id.get("sub")

        if not user_id:
            print(f"DEBUG REFRESH: Payload sem sub válido: {payload}")
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return create_tokens(str(user_id))
    
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )