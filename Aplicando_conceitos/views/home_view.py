from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings

router = APIRouter()

#Criando rota index
"""@router.get('/', name="index")
async def index(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('home/index.html', context=context)

#Criando rota about
@router.get('/about', name="about")
async def about(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('about/about.html', context=context)

    """