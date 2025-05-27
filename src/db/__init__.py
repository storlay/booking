__all__ = (
    "Base",
    "Hotels",
    "Rooms",
)

from src.db.database import Base
from src.models.hotels import Hotels
from src.models.rooms import Rooms