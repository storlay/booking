from src.db import Base
from src.db.mixins import IntPkModelMixin

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Hotels(Base, IntPkModelMixin):
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(1000))
