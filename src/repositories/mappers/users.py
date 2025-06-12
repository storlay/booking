from src.models.users import Users
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.users import UserSchema


class UsersDataMapper(BaseDataMapper):
    schema = UserSchema
    model = Users
