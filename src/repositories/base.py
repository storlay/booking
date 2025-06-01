from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Base


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

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
        # fmt: off
        return [
            self.schema.model_validate(model)
            for model in result.scalars().all()
        ]
        # fmt: on

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
        model = result.scalars().one_or_none()
        if model is None:
            return model
        return self.schema.model_validate(model)

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
        model = result.scalar_one()
        return self.schema.model_validate(model)

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
