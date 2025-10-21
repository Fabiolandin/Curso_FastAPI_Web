from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles


from views.admin import admin_view
#from views import home_view

#Configuração do FastAPI, desabilitando a documentação automática
app = FastAPI(docs_url=None, redoc_url=None)

#Definindo o diretório para arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


#Incluindo as rotas do admin_view
app.include_router(admin_view.router)

#Criando rota index
@app.get('/')
async def index(request: Request, usuario: str = 'Fabio Landin'):
    context = {
        "request": request,
        "usuario": usuario
    }

    return settings.TEMPLATES.TemplateResponse('index.html', context=context)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)