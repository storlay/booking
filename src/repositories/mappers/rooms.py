from src.models.rooms import Rooms
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.rooms import RoomSchema
from src.schemas.rooms import RoomWithRelsSchema


class RoomsDataMapper(BaseDataMapper):
    schema = RoomSchema
    schema_with_rels = RoomWithRelsSchema
    model = Rooms
