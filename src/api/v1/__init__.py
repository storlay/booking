from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.bookings import router as bookings_router
from src.api.v1.facilities import router as facilities_router
from src.api.v1.hotels import router as hotels_router
from src.api.v1.rooms import router as rooms_router


router_v1 = APIRouter(
    prefix="/v1",
)

routers = (
    auth_router,
    hotels_router,
    rooms_router,
    facilities_router,
    bookings_router,
)

for router in routers:
    router_v1.include_router(router)
