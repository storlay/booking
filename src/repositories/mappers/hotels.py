from src.models.hotels import Hotels
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.hotels import HotelSchema


class HotelsDataMapper(BaseDataMapper):
    schema = HotelSchema
    model = Hotels
