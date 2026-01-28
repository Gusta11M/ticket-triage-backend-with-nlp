
from http.client import HTTPException, status
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession

async def authenticate_user(db : AsyncSession, email: str, password: str):

    user = await get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    return create_access_token(subject=str(user.id))