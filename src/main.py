from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api import main_router
from src.setup import redis_manager


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager.redis),
        prefix="cache",
    )
    yield
    await redis_manager.disconnect()


app = FastAPI(
    title="Booking API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
)

app.include_router(main_router)
