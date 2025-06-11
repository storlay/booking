from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Base


class BaseRepository:
    model: type[Base] = None
    schema: BaseModel = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_filtered(
        self,
        limit: int = None,
        offset: int = None,
        *filter,
        **filter_by,
    ) -> list[BaseModel | Any]:
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        if limit and offset:
            query = (
                query
                .limit(limit)
                .offset(offset)
            )

        result = await self.session.execute(query)
        # fmt: off
        return [
            self.schema.model_validate(model)
            for model in result.scalars().all()
        ]
        # fmt: on

    async def get_all(
        self,
        limit: int,
        offset: int,
        *args,
        **kwargs,
    ) -> list[BaseModel | Any]:
        return await self.get_filtered(
            limit=limit,
            offset=offset,
        )

    async def get_one_or_none(
        self,
        **filter_by,
    ) -> BaseModel | None | Any:
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return model
        return self.schema.model_validate(model)

    async def get_one(
        self,
        **filter_by,
    ) -> BaseModel | Any:
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        result = await self.session.execute(query)
        model = result.scalar_one()
        return self.schema.model_validate(model)

    async def add(
        self,
        data: BaseModel,
    ) -> BaseModel | Any:
        # fmt: off
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model)

    async def add_bulk(
        self,
        data: list[BaseModel],
    ) -> None:
        # fmt: off
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        # fmt: on
        await self.session.execute(stmt)

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
