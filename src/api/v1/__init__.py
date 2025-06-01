from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.hotels import router as hotels_router


router_v1 = APIRouter(
    prefix="/v1",
)

routers = (
    auth_router,
    hotels_router,
)

for router in routers:
    router_v1.include_router(router)
