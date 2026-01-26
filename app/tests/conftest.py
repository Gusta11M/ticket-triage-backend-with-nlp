from dotenv import load_dotenv
import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.db.base import Base
from app.db.dependencies import get_db
import os
import sys

# Importação explícita para garantir que o SQLAlchemy mapeia as relações
from app.models import category, priority, user, ticket

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Configuração do ProactorEventLoop para Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

engine_test = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool,
    isolation_level="AUTOCOMMIT",
    echo=False
)

TestingSessionLocal = sessionmaker(
    engine_test, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Event loop com escopo de função (mais seguro para pytest-asyncio)
@pytest.fixture(scope="function")
def event_loop():
    """Cria um novo loop para cada teste."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    
    # Cancela todas as tarefas pendentes
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    
    # Aguarda o cancelamento
    if pending:
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    """Configuração única do banco de dados para toda a sessão."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine_test.dispose()

@pytest.fixture
async def db_session():
    """Fornece uma sessão de banco de dados isolada para cada teste."""
    async with TestingSessionLocal() as session:
        # Limpeza antes do teste
        await session.execute(text('TRUNCATE TABLE "Ticket", "Category", "Priority", "User" RESTART IDENTITY CASCADE'))
        await session.commit()
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Fornece um cliente HTTP de teste com sessão de BD sobrescrita."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()