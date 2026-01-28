import token
from fastapi import APIRouter, Depends
from app.services.auth import register
from app.db.dependencies import get_db
from app.schemas.auth import LoginRequest, RefreshTokenRequest, RegisterRequest, TokenResponse
from app.services.auth import authenticate_user, refresh_tokens
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register_endpoint(
    data : RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    token, refresh_token = await register(db, data)
    return {"access_token": token, "refresh_token": refresh_token}

@router.post("/login", response_model=TokenResponse)
async def login(
    data : LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    token , refresh_token = await authenticate_user(db, data)
    return {"access_token": token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=TokenResponse)
def refresh(
    data : RefreshTokenRequest
):
    access_token, refresh_token = refresh_tokens(data)
    return {"access_token": access_token, "refresh_token": refresh_token}