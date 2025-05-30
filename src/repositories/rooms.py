from src.models.rooms import Rooms
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = Rooms
