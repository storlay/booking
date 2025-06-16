from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.bookings import BookingsDataMapper


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
