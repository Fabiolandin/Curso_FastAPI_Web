from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey


class ProdutoModel(settings.DBBaseModel):
    """Tabela de produtos"""
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey("categoria_produto.id"), nullable=False)

    # relacionamentos
    categoria: Mapped["CategoriaProdutoModel"] = relationship("CategoriaProdutoModel", back_populates="produto")
    item_pedido: Mapped[list["ItemPedidoModel"]] = relationship("ItemPedidoModel", back_populates="produto")
