from typing import Any
from typing import Iterable

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.db.database import Base
from src.repositories.mappers.base import BaseDataMapper


class BaseRepository:
    model: type[Base] = None
    mapper: type[BaseDataMapper] = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_filtered(
        self,
        limit: int = None,
        offset: int = None,
        query_options: Iterable[ExecutableOption] | None = None,
        *filter,
        with_rels: bool = False,
        **filter_by,
    ) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if query_options is not None:
            query = query.options(*query_options)
        if limit:
            query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        models = (
            result.scalars().unique().all()
            if query_options is not None
            else result.scalars().all()
        )
        # fmt: off
        return [
            self.mapper.map_to_domain_entity(model, with_rels=with_rels)
            for model in models
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
        return self.mapper.map_to_domain_entity(model)

    async def get_one(
        self,
        query_options: Iterable[ExecutableOption] | None = None,
        with_rels: bool = False,
        **filter_by,
    ) -> BaseModel | Any:
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        if query_options is not None:
            query = query.options(*query_options)
        result = await self.session.execute(query)
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model, with_rels=with_rels)

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
        return self.mapper.map_to_domain_entity(model)

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
    ) -> int:
        # fmt: off
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=partially))
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_one(
        self,
        **filter_by,
    ) -> int:
        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete_bulk(
        self,
        **filter_by,
    ) -> None:
        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        await self.session.execute(stmt)
