from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings

router = APIRouter()

#Criando rota index
@router.get('/', name="index")
async def index(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('home/index.html', context=context)

#Criando rota cliente
@router.get('/cliente', name="cliente")
async def cliente(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('home/cliente.html', context=context)

#Criando rota produto
@router.get('/produto', name="produto")
async def produto(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('home/produto.html', context=context)

