from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


#Instanciando FASTAPI e colocando na variavel APP, e fazendo o mesmo para resRender Jinja2
app = FastAPI()
templates = Jinja2Templates(directory='templates')
# Nessa aplicação monte para min o /static com o diretorio static com nome de montagem static
app.mount('/static', StaticFiles(directory='static'), name='static')

#Criando a rota index e retornando o index.html como view
@app.get('/')
async def index(request: Request, usuario: str = 'Felicity Jones'):
    context = {
        "request": request,
        "usuario": usuario
    }

    return templates.TemplateResponse('index.html', context=context) # tudo que for passado dentro de context poderá ser usado no template index.html

#Criando a rota para /servicos, e retornando servicos.html como view
@app.get('/servicos')
async def servicos(request: Request, usuario: str = 'Felicity Jones'):
    context = {
        "request": request
    }

    return templates.TemplateResponse('servicos.html', context=context)

@app.post('/servicos')
async def cad_servicos(request: Request):
    form = await request.form()

    servico: str = form.get('servico')

    print(f'Serviço: {servico}')
    context = {
        "request": request
    }

    return templates.TemplateResponse('servicos.html', context=context)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)