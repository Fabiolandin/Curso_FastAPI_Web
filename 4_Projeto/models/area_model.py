from core.configs import settings

from sqlalchemy import Column, Integer, String

class AreaModel(settings.DBBaseModel):
    """ Dúvidas respondidas no FAQ são categorias em áreas """
    __tablename__ = 'areas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    area: str = Column(String(100))