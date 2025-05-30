from src.models.hotels import Hotels
from src.repositories.base import BaseRepository

from sqlalchemy import select


class HotelsRepository(BaseRepository):
    model = Hotels

    async def get_all(
        self,
        title: str | None,
        location: str | None,
        limit: int,
        offset: int,
    ):
        query = select(Hotels)
        if title:
            query = query.filter(Hotels.title.icontains(title))
        if location:
            query = query.filter(Hotels.location.icontains(location))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
