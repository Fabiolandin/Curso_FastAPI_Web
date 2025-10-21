from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class FuncionarioModel(settings.DBBaseModel):
    """Tabela de funcionários"""
    __tablename__ = 'funcionario'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    cpf: Mapped[str] = mapped_column(String(18))
    cargo: Mapped[str] = mapped_column(String(50))
    data_admissao: Mapped[str] = mapped_column(String(15))

    pedidos: Mapped[list["PedidoModel"]] = relationship("PedidoModel", back_populates="funcionario")
    compras: Mapped[list["CompraModel"]] = relationship("CompraModel", back_populates="funcionario")
