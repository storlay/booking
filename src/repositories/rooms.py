from datetime import date

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = RoomSchema

    async def get_available_for_hotel(
        self,
        hotel_id: int,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
    ) -> list[RoomSchema]:
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from,
            date_to,
            hotel_id,
        )
        filters = [
            Rooms.id.in_(rooms_ids_to_get),
        ]
        return await self.get_filtered(
            limit,
            offset,
            *filters,
        )
