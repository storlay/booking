from fastapi import APIRouter

from src.api.v1 import router_v1

routers = (router_v1,)

main_router = APIRouter()

for router in routers:
    main_router.include_router(router)
