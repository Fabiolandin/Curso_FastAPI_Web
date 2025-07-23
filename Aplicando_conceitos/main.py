from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates') #falando pro jinja renderizar os arquivos do diretório templates

#Criando rota index
@app.get('/')
async def index(request: Request, usuario: str = 'Fabio Landin'):
    context = {
        "request": request,
        "usuario": usuario
    }

    return templates.TemplateResponse('index.html', context=context)

#Criando rota produto
@app.get('/produto')
async def produto(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse('produto.html', context=context)

#Criando rota para cliente
@app.get('/cliente')
async def cliente(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse('cliente.html', context=context)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)