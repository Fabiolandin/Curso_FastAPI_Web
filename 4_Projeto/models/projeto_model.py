from datetime import datetime

from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime

class ProjetoModel(settings.DBBaseModel):
    """No website temos um portfólio de projetos"""
    __tablename__ = 'projetos'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descricao_inicial: Mapped[str] = mapped_column(String(300))
    imagem1: Mapped[str] = mapped_column(String(100))  # 1300x700
    imagem2: Mapped[str] = mapped_column(String(100))  # 600x400
    imagem3: Mapped[str] = mapped_column(String(100))  # 600x400
    descricao_final: Mapped[str] = mapped_column(String(300))
    link: Mapped[str] = mapped_column(String(200))