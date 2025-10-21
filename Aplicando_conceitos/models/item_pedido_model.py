from core.configs import settings
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ItemPedidoModel(settings.DBBaseModel):
    __tablename__ = "item_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    pedido_id: Mapped[int] = mapped_column(Integer, ForeignKey("pedido.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(Integer, ForeignKey("produto.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped["PedidoModel"] = relationship("PedidoModel", back_populates="item_pedido")
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel", back_populates="item_pedido")