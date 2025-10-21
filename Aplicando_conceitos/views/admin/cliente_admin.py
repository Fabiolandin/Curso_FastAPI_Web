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

router = APIRouter(prefix="/cliente")

#Criando rota para cliente
@router.get('/')
async def cliente(request: Request):
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('admin/cliente.html', context=context)

#Post de cliente / receber dados do formulario
@router.post('/')
async def cad_cliente(request: Request):
    form = await request.form()

    nome: str = form.get('nome')
    idade: int = form.get('idade')
    cpf: str = form.get('cpf')

    print(f'Nome: {nome}, Idade: {idade}, CPF: {cpf}')

    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('admin/cliente.html', context=context)