from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey
from datetime import datetime

class PedidoModel(settings.DBBaseModel):
    """ Table de Pedidos """
    __tablename__ = 'pedido'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('cliente.id'), nullable=False)
    funcionario_id: Mapped[int] = mapped_column(Integer, ForeignKey('funcionario.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='Pendente')
    valor_total: Mapped[float] = mapped_column(Float, default=0.0)
    data_pedido: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    cliente: Mapped["ClienteModel"] = relationship("ClienteModel", back_populates="pedido")
    funcionario: Mapped["FuncionarioModel"] = relationship("FuncionarioModel", back_populates="pedidos")
    item_pedido: Mapped[list["ItemPedidoModel"]] = relationship("ItemPedidoModel", back_populates="pedido")
