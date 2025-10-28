from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from datetime import datetime

class ClienteModel(settings.DBBaseModel):
    """ Table de cientes """
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(100))
    data_de_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    pedido: Mapped[list["PedidoModel"]] = relationship("PedidoModel", back_populates="cliente")