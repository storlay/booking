from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db import Base
from src.db.mixins import IntPkModelMixin


if TYPE_CHECKING:
    from src.models.rooms import Rooms


class Facilities(Base, IntPkModelMixin):
    title: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )

    rooms: Mapped[list["Rooms"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )

    def __repr__(self):
        return f"<Facility id={self.id!r}, title={self.title!r}>"


class RoomsFacilities(Base, IntPkModelMixin):
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
    )
    facility_id: Mapped[int] = mapped_column(
        ForeignKey("facilities.id"),
    )

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "facility_id",
            name="uq_room_facility",
        ),
    )
