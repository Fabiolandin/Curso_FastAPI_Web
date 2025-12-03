from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class FornecedorModel(settings.DBBaseModel):
    """ Table de fornecedor """
    __tablename__ = 'fornecedor'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    cpf_cpnj: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(100))

    compra: Mapped[list["CompraModel"]] = relationship("CompraModel", back_populates="fornecedor")