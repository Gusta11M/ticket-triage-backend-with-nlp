import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ========== CONFIGURAÇÃO CORRETA DO ENGINE ==========
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_recycle=3600,   # Recicla conexões após 1 hora
)

# ========== SESSIONMAKER COM CONFIGURAÇÕES ADEQUADAS ==========
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,  # Desabilita autoflush para maior controle
)