from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Integer
from core.configs import settings

class MembroModel(settings.DBBaseModel):
    __tablename__ = 'membros'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    funcao: Mapped[str] = mapped_column(String(100))
    imagem: Mapped[str] = mapped_column(String(100))

    @validates('funcao')
    def _validate_funcao(self, key, value):
        if value is None or value == '':
            raise ValueError("Você precisa informar uma função válida.")
        if 'Python' not in value:
            raise ValueError("A função deve conter a palavra 'Python'.")
        return