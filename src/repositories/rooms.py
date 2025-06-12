from datetime import date

from pydantic import BaseModel
from sqlalchemy.orm import selectinload

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.repositories.mappers.rooms import RoomsDataMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = Rooms
    mapper = RoomsDataMapper

    async def get_available_for_hotel(
        self,
        hotel_id: int,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
    ) -> list[type[BaseModel]]:
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from,
            date_to,
            hotel_id,
        )
        filters = [
            Rooms.id.in_(rooms_ids_to_get),
        ]
        query_options = [
            selectinload(self.model.facilities),
        ]
        return await self.get_filtered(
            limit,
            offset,
            query_options,
            *filters,
        )

    async def get_one_with_full_info(
        self,
        **filter_by,
    ) -> type[BaseModel]:
        query_options = [
            selectinload(self.model.facilities),
        ]
        return await self.get_one(
            query_options,
            **filter_by,
        )
