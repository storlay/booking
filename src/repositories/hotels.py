from datetime import date

from sqlalchemy import select

from src.models.hotels import Hotels
from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.mappers.hotels import HotelsDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = Hotels
    mapper = HotelsDataMapper

    def get_with_available_rooms(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        filters: list[str | None],
    ):
        available_rooms_ids = rooms_ids_for_booking(
            date_from,
            date_to,
        )
        hotels_ids = (
            select(Rooms.hotel_id)
            .select_from(Rooms)
            .filter(Rooms.id.in_(available_rooms_ids))
        )
        filters = filters + [Hotels.id.in_(hotels_ids)]
        return self.get_filtered(
            limit,
            offset,
            *filters,
        )
