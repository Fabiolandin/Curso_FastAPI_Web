from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

#Configuração do FastAPI, desabilitando a documentação automática
app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory="templates")

#Definindo o diretório para arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

#Criando rota index
@app.get('/')
async def index(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse('home/index.html', context=context)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", debug=True)