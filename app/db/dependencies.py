from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal

async def get_db() -> AsyncSession:
    """
    Dependency que fornece uma sessão de banco de dados.
    Garante que a sessão é fechada após o uso.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()