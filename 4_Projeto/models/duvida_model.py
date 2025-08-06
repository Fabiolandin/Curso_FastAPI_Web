from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.configs import settings
from models.area_model import AreaModel
from sqlalchemy import Integer, String, ForeignKey

class DuvidaModel(settings.DBBaseModel):
    __tablename__ = 'duvida'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_area: Mapped[int] = mapped_column(ForeignKey('areas.id'))
    area: Mapped["AreaModel"] = relationship('AreaModel', lazy='joined')

    titulo: Mapped[str] = mapped_column(String(200))
    resposta: Mapped[str] = mapped_column(String(400))
    

