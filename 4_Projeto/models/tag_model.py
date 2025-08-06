from core.configs import settings
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class TagModel(settings.DBBaseModel):
    """Temos tags em várias partes do website"""
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(String(100))