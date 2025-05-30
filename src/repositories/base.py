from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all(
        self,
        *args,
        **kwargs,
    ):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(
        self,
        **filter_by,
    ):
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(
        self,
        data: BaseModel,
    ):
        # fmt: off
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_one(
        self,
        data: BaseModel,
        partially: bool = False,
        **filter_by,
    ) -> None:
        # fmt: off
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=partially))
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        result.one()

    async def delete_one(
        self,
        **filter_by,
    ) -> None:
        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        result.one()
