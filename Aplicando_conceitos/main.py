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

#Post de produto / receber dados do formulario
@app.post('/produto')
async def cad_produto(request: Request):
    form = await request.form()

    nome: str = form.get('nome')
    descricao: str = form.get('descricao')
    quantidade: int = form.get('quantidade')

    print(f'Produto: {nome}, Descrição: {descricao}, Quantidade: {quantidade}')

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

#Post de cliente / receber dados do formulario
@app.post('/cliente')
async def cad_cliente(request: Request):
    form = await request.form()

    nome: str = form.get('nome')
    idade: int = form.get('idade')
    cpf: str = form.get('cpf')

    print(f'Nome: {nome}, Idade: {idade}, CPF: {cpf}')

    context = {
        "request": request
    }

    return templates.TemplateResponse('cliente.html', context=context)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)