from src.models.users import Users
from src.repositories.base import BaseRepository
from src.schemas.users import UserSchema


class UsersRepository(BaseRepository):
    model = Users
    schema = UserSchema
