from datetime import datetime

from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings
from views.admin import produto_admin
from views.admin.cliente_admin import cliente_admin
from views.admin.categoria_produto_admin import categoria_produto_admin

router = APIRouter(prefix='/admin')

#Rotas admin
router.include_router(produto_admin.router, prefix='/admin')
router.include_router(cliente_admin.router, prefix='/admin')
router.include_router(categoria_produto_admin.router, prefix='/admin')


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    """ Rota para o index do admin """
    context = {'request': request, "ano": datetime.now().year}
    return settings.TEMPLATES.TemplateResponse("admin/index.html", context=context)