from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from core.configs import settings

#Passando o URL do banco para a criação do engine e pedindo para não exibir os logs SQL
engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=False)

#Cria a sessão porém não fecha "async with get_session() as session:" já se encarrega de fechar
def get_session() -> AsyncSession:
    __async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
        bind=engine
    )

    session: AsyncSession = __async_session()
    
    return session


async def create_tables() -> None:
    import models.__all_models
    print('Criando tabelas...')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')