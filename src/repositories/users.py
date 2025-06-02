from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import Users
from src.repositories.base import BaseRepository
from src.schemas.users import UserSchema
from src.schemas.users import UserWithPasswordSchema


class UsersRepository(BaseRepository):
    model = Users
    schema = UserSchema

    async def get_one_with_password(
        self,
        email: EmailStr,
    ) -> UserWithPasswordSchema | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalar_one()
        return UserWithPasswordSchema.model_validate(model)
