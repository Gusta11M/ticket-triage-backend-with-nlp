from dotenv import load_dotenv
import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.db.session import Base
from app.db.dependencies import get_db
import os

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine_test = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool,
    isolation_level="AUTOCOMMIT"
)

TestingSessionLocal = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    await engine_test.dispose()

@pytest.fixture
async def client():
    async with TestingSessionLocal() as session:
        await session.execute(text('TRUNCATE TABLE "Ticket", "User", "Category", "Priority" RESTART IDENTITY CASCADE'))
        
        await session.commit()

        app.dependency_overrides[get_db] = lambda: session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
        
        app.dependency_overrides.clear()
        await session.close()