from sqlalchemy import select

from src.models.hotels import Hotels
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = Hotels
    schema = HotelSchema

    async def get_all(
        self,
        title: str | None,
        location: str | None,
        limit: int,
        offset: int,
    ) -> list[HotelSchema]:
        query = select(Hotels)
        if title:
            query = query.filter(Hotels.title.icontains(title))
        if location:
            query = query.filter(Hotels.location.icontains(location))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        # fmt: off
        return [
            self.schema.model_validate(model)
            for model in result.scalars().all()
        ]
        # fmt: on
