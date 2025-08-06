from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import ClassVar 
from sqlalchemy.orm import DeclarativeBase

class Settings(BaseSettings):
    DB_URL: str = 'mysql+asyncmy://root:@localhost:3306/fastapi_web'
    DBBaseModel: ClassVar[DeclarativeBase] = declarative_base()  # Anotação corrigida
    TEMPLATES: ClassVar[Jinja2Templates] = Jinja2Templates(directory='templates')
    MEDIA: ClassVar[Path] = Path('media')

    class Config:
        case_sensitive = True

settings: Settings = Settings()