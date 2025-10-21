from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer


class CategoriaProdutoModel(settings.DBBaseModel):
    """Tabela de categorias de produtos"""
    __tablename__ = "categoria_produto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)

    # relacionamento com Produto
    produto: Mapped[list["ProdutoModel"]] = relationship("ProdutoModel", back_populates="categoria")
