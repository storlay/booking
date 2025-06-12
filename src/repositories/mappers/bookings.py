from src.models.bookings import Bookings
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.bookings import BookingSchema


class BookingsDataMapper(BaseDataMapper):
    schema = BookingSchema
    model = Bookings
