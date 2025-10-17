from typing import List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.configs import settings
from models.tag_model import TagModel
from models.autor_model import AutorModel
from models.comentario_model import ComentarioModel

from sqlalchemy import Table, Integer, String, DateTime, ForeignKey, Column

# Post pode ter várias tags
tags_post = Table(
    'tags_post',
    settings.DBBaseModel.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_tag', Integer, ForeignKey('tags.id'))
)

# Post pode ter vários comentários
comentarios_post = Table(
    'comentarios_post',
    settings.DBBaseModel.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_comentario', Integer, ForeignKey('comentarios.id'))
)

class PostModel(settings.DBBaseModel):
    """Posts do blog"""
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200))
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    # Um Post pode ter várias tags
    tags: Mapped[List[TagModel]] = relationship(
        'TagModel',
        secondary=tags_post,
        backref='tagp',
        lazy='joined'
    )

    imagem: Mapped[str] = mapped_column(String(100))  # 900x400
    texto: Mapped[str] = mapped_column(String(1000))

    # Um Post pode ter vários comentários
    comentarios: Mapped[List[object]] = relationship(
        'ComentarioModel',
        secondary=comentarios_post,
        backref='comentario',
        lazy='joined'
    )

    id_autor: Mapped[int] = mapped_column(ForeignKey('autores.id'))
    autor: Mapped[AutorModel] = relationship('AutorModel', lazy='joined')