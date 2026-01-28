from sqlalchemy import select
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import RegisterRequest

async def create_user(db: AsyncSession, data: RegisterRequest) -> User:
    new_user = User(
        email=data.email,
        hashed_password=data.password,
        role=data.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalars().first()