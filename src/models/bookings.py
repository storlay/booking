from datetime import date
from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.config.config import settings
from src.db.database import Base
from src.db.mixins import IntPkModelMixin


class Bookings(Base, IntPkModelMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
    )
    date_from: Mapped[date]
    date_to: Mapped[date]
    price_per_day: Mapped[Decimal] = mapped_column(
        DECIMAL(
            precision=settings.models.DECIMAL_PRECISION,
            scale=settings.models.DECIMAL_SCALE,
        )
    )

    @hybrid_property
    def total(self) -> Decimal:
        return self.price_per_day * (self.date_to - self.date_from).days

    __table_args__ = (
        CheckConstraint(
            "date_to >= date_from",
            name="check_booking_date",
        ),
        CheckConstraint(
            "price_per_day >= 0",
            name="check_booking_price",
        ),
    )
