from sqlalchemy import select

from src.models.rooms import Rooms
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = RoomSchema

    async def get_all_for_hotel(
        self,
        hotel_id: int,
        limit: int,
        offset: int,
    ) -> list[RoomSchema]:
        # fmt: off
        query = (
            select(Rooms)
            .filter_by(hotel_id=hotel_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model)
            for model in result.scalars().all()
        ]
        # fmt :on
