from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.config import settings
from src.db import Base
from src.db.mixins import IntPkModelMixin


if TYPE_CHECKING:
    from src.models.facilities import Facilities


class Rooms(Base, IntPkModelMixin):
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id"),
    )
    title: Mapped[str] = mapped_column(
        String(100),
    )
    description: Mapped[str | None] = mapped_column(
        Text,
    )
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(
            precision=settings.models.DECIMAL_PRECISION,
            scale=settings.models.DECIMAL_SCALE,
        ),
    )
    quantity: Mapped[int]

    facilities: Mapped[list["Facilities"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",
    )

    def __repr__(self):
        return f"<Room id={self.id!r}, title={self.title!r}>"

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="check_room_price",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="check_room_quantity",
        ),
    )
