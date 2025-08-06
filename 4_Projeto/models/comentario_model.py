from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey

from core.configs import settings
from models.post_model import PostModel

class ComentarioModel(settings.DBBaseModel):
    __tablename__ = 'comentarios'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    id_post: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped["PostModel"] = relationship('PostModel', lazy='joined')

    autor: Mapped[str] = mapped_column(String(200))
    texto: Mapped[str] = mapped_column(String(500))