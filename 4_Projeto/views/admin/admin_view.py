from datetime import datetime

from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings
from views.admin.membro_admin import membro_admin

router = APIRouter(prefix='/admin')
router.include_router(membro_admin.router, prefix='/admin')


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    """ Rota para o index do admin """
    context = {'request': request, "ano": datetime.now().year}
    return settings.TEMPLATES.TemplateResponse("admin/index.html", context=context)