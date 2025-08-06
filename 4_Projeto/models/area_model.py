from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class AreaModel(settings.DBBaseModel):
    """ Dúvidas respondidas no FAQ são categorias em áreas """
    __tablename__ = 'areas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    area: Mapped[str] = mapped_column(String(100))