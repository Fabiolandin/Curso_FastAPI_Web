from core.configs import settings
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ItemCompraModel(settings.DBBaseModel):
    __tablename__ = "item_compra"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    compra_id: Mapped[int] = mapped_column(ForeignKey("compra.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    compra: Mapped["CompraModel"] = relationship("CompraModel", back_populates="item_compra")
    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel", back_populates="item_compra")
