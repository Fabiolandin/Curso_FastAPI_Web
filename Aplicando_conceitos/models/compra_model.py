from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Float, Integer, ForeignKey
from datetime import datetime

class CompraModel(settings.DBBaseModel):
    """ Table de Compras """
    __tablename__ = 'compra'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fornecedor_id: Mapped[int] = mapped_column(Integer, ForeignKey('fornecedor.id'), nullable=False)
    funcionario_id: Mapped[int] = mapped_column(Integer, ForeignKey('funcionario.id'), nullable=False)
    data_compra: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    valor_total: Mapped[float] = mapped_column(Float, default=0.0)

    fornecedor: Mapped["FornecedorModel"] = relationship("FornecedorModel", back_populates="compra")
    funcionario: Mapped["FuncionarioModel"] = relationship("FuncionarioModel", back_populates="compras")
    item_compra: Mapped[list["ItemCompraModel"]] = relationship("ItemCompraModel", back_populates="compra")
