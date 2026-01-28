
from select import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.dependencies import get_db
from app.models.user import User
from app.core.config import settings
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession


oauht2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauht2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        
        result = await db.execute(
            select(User).where(User.id == int(user_id))
        )
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    
        return user

    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    

    return user