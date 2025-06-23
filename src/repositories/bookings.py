from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.exceptions.repository.bookings import RoomUnavailableRepoException
from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.bookings import BookingsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingCreateSchema


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingsDataMapper

    async def get_bookings_for_notify_checkin(self) -> list[type[BaseModel]]:
        # fmt: off
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]
        # fmt: on

    async def add_booking(
        self,
        data: BookingCreateSchema,
        hotel_id: int,
    ):
        rooms_ids_query = rooms_ids_for_booking(
            data.date_from,
            data.date_to,
            hotel_id,
        )
        result = await self.session.execute(rooms_ids_query)
        available_rooms_ids = result.scalars().all()
        if data.room_id not in available_rooms_ids:
            raise RoomUnavailableRepoException
        return await self.add(data)
