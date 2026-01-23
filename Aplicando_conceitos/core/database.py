from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from core.configs import settings

#Passando o URL do banco para a criação do engine e pedindo para não exibir os logs SQL
engine: AsyncEngine = create_async_engine(
    settings.DB_URL, 
    echo=False,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_recycle=3600,   # Recicla conexões a cada hora
)

#Cria o sessionmaker uma única vez
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

#Cria a sessão e garante que ela será fechada corretamente após o uso
@asynccontextmanager
async def get_session() -> AsyncSession:
    session: AsyncSession = async_session()
    
    try:
        yield session
    finally:
        await session.close()  # Garante que a sessão será fechada mesmo em caso de erro


async def create_tables() -> None:
    import models.__all_models
    print('Criando tabelas...')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')