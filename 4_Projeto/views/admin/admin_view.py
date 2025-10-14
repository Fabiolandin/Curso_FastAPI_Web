from datetime import datetime

from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings
from views.admin.membro_admin import membro_admin
from views.admin.autor_admin import autor_admin
from views.admin.tag_admin import tag_admin
from views.admin.area_admin import area_admin

router = APIRouter(prefix='/admin')
#Rotas admin
router.include_router(membro_admin.router, prefix='/admin')
router.include_router(autor_admin.router, prefix='/admin')
router.include_router(tag_admin.router, prefix='/admin')
router.include_router(area_admin.router, prefix='/admin')


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    """ Rota para o index do admin """
    context = {'request': request, "ano": datetime.now().year}
    return settings.TEMPLATES.TemplateResponse("admin/index.html", context=context)