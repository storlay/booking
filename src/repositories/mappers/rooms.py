from src.models.rooms import Rooms
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.rooms import RoomSchema


class RoomsDataMapper(BaseDataMapper):
    schema = RoomSchema
    model = Rooms
