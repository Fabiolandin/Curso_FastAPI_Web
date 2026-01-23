from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import models.__all_models

from core.database import engine
from views.admin import admin_view
from views import home_view


#Gerenciamento do ciclo de vida da aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: aplicação está iniciando
    yield
    # Shutdown: aplicação está sendo encerrada
    await engine.dispose()  # Fecha todas as conexões do pool


#Configuração do FastAPI, desabilitando a documentação automática
app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

#Definindo o diretório para arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


#Incluindo as rotas do admin_view
app.include_router(admin_view.router)
app.include_router(home_view.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)