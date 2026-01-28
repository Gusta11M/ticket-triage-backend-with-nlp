from fastapi import APIRouter, Depends
from app.db.dependencies import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    data : LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    token = await authenticate_user(db, data.username, data.password)

    return {"access_token": token}
