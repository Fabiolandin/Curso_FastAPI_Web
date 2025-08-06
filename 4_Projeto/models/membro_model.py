from sqlalchemy import Column, Integer, String
from core.configs import settings

class MembroModel(settings.DBBaseModel):
    __tablename__ = 'membros'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    funcao: str = Column(String(100))
    imagem: str = Column(String(100))

    @validates('funcao')
    def _validate_funcao(self, key, value):
        if value is None or value == '':
            raise ValueError("Você precisa informar uma função válida.")
        if 'Python' not in value:
            raise ValueError("A função deve conter a palavra 'Python'.")
        return value