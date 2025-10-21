from datetime import datetime
from typing import List

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
#from controllers.autor_controller import AutorController
#from views.admin.base_crud_view import BaseCRUDView

router = APIRouter(prefix="/produto")

#Criando rota produto
@router.get('/')
async def produto(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('admin/produto.html', context=context)

#Post de produto / receber dados do formulario
@router.post('/')
async def cad_produto(request: Request):
    form = await request.form()

    nome: str = form.get('nome')
    descricao: str = form.get('descricao')
    quantidade: int = form.get('quantidade')

    print(f'Produto: {nome}, Descrição: {descricao}, Quantidade: {quantidade}')

    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('admin/produto.html', context=context)