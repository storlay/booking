from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db import Base
from src.db.mixins import IntPkModelMixin


class Hotels(Base, IntPkModelMixin):
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(1000))

    def __repr__(self):
        return f"<Hotel id={self.id!r}, title={self.title!r}>"
