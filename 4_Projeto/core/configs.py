from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import ClassVar 
from sqlalchemy.orm import DeclarativeBase

class Settings(BaseSettings):
    #URL do banco de dados que voce vai utilizar, lembrando que ja o banco ja deve estar criado no DBeaver
    DB_URL: str = 'mysql+asyncmy://root:@localhost:3306/fastapi_web'
    #Para fazer uso das classes do SQLAlchemy
    DBBaseModel: ClassVar[DeclarativeBase] = declarative_base()
    #Para fazer uso dos templates do Jinja2
    TEMPLATES: ClassVar[Jinja2Templates] = Jinja2Templates(directory='templates')
    #Caminho para a pasta de midia
    MEDIA: ClassVar[Path] = Path('media')

    #Diferença entre letras maiusculas e minusculas e queremos que esteja no banco de dados
    class Config:
        case_sensitive = True

#Instancia unica da classe Settings
settings: Settings = Settings()