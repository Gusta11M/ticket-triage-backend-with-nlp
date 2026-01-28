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

# ========== SOLUÇÃO: Engine global sem conexões persistentes ==========
engine_test = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool,
    echo=False
)

# ========== MUDANÇA 1: Remover o fixture de event_loop customizado ==========
# Deixar o pytest-asyncio gerenciar o event loop automaticamente

# ========== MUDANÇA 2: Setup do BD síncrono executado uma vez ==========
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Setup e teardown do schema do banco - executado de forma síncrona."""
    import asyncio
    
    async def create_tables():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine_test.dispose()
    
    # Cria um novo loop temporário para setup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_tables())
    loop.close()
    
    yield
    
    # Cria um novo loop temporário para teardown
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(drop_tables())
    loop.close()

# ========== MUDANÇA 3: Sessão de BD recriada para cada teste ==========
@pytest.fixture
async def db_session():
    """Fornece uma sessão de banco de dados isolada para cada teste."""
    # Cria uma nova sessão para cada teste
    async_session = sessionmaker(
        engine_test, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        # Limpeza antes do teste
        try:
            await session.execute(text('TRUNCATE TABLE "Ticket", "Category", "Priority", "User" RESTART IDENTITY CASCADE'))
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Erro ao limpar tabelas: {e}")
        
        yield session
        
        # Rollback ao final
        try:
            await session.rollback()
        except Exception:
            pass

@pytest.fixture
async def client(db_session):
    """Fornece um cliente HTTP de teste com sessão de BD sobrescrita."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()

async def get_token_for_user(client: AsyncClient, email: str, role: str):
    """Função auxiliar para registar e logar utilizadores nos testes."""
    password = "Password123"
    
    # 1. Tentar registar
    reg_response = await client.post("/auth/register", json={
        "email": email,
        "password": password,
        "role": role
    })
    
    # 2. Login como Form Data (OAuth2 padrão)
    login_data = {"username": email, "password": password}
    response = await client.post("/auth/login", data=login_data)

    # 3. Se falhar, tenta como JSON
    if response.status_code != 200:
        response = await client.post("/auth/login", json={
            "email": email, 
            "password": password
        })

    if response.status_code != 200:
        print(f"\n❌ FALHA NO LOGIN ({email}): {response.status_code}")
        print(f"Response: {response.text}")
        return None

    token_data = response.json()
    return token_data.get("access_token")

@pytest.fixture
async def admin_headers(client: AsyncClient):
    """Headers com token de administrador."""
    token = await get_token_for_user(client, "admin@test.com", "admin")
    if not token:
        pytest.fail("❌ Não foi possível obter token de Admin")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def user_headers(client: AsyncClient):
    """Headers com token de utilizador normal."""
    token = await get_token_for_user(client, "user@test.com", "user")
    if not token:
        pytest.fail("❌ Não foi possível obter token de User")
    return {"Authorization": f"Bearer {token}"}