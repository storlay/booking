from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import Users
from src.repositories.base import BaseRepository
from src.repositories.mappers.users import UsersDataMapper
from src.schemas.users import UserWithPasswordSchema


class UsersRepository(BaseRepository):
    model = Users
    mapper = UsersDataMapper

    async def get_one_or_none_with_password(
        self,
        email: EmailStr,
    ) -> UserWithPasswordSchema | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return UserWithPasswordSchema.model_validate(model)
