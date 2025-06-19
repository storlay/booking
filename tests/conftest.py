import json

import aiofiles
import pytest
from httpx import ASGITransport
from httpx import AsyncClient

from src.config import settings
from src.db.database import Base
from src.db.database import async_engine_null_pull
from src.db.database import async_session_null_pool
from src.main import app
from src.schemas.hotels import HotelCreateOrUpdateSchema
from src.schemas.rooms import RoomCreateSchema
from src.utils.transaction import TransactionManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.app.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def prepare_db(check_test_mode):
    async with async_engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def db(prepare_db):
    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        yield transaction


@pytest.fixture(scope="session")
async def populate_db(db):
    async with aiofiles.open(
        "tests/mock_hotels.json",
        "r",
        encoding="utf-8",
    ) as hotels_file:
        content = await hotels_file.read()
        hotels_data = json.loads(content)

    async with aiofiles.open(
        "tests/mock_rooms.json",
        "r",
        encoding="utf-8",
    ) as rooms_file:
        content = await rooms_file.read()
        rooms_data = json.loads(content)

    # fmt: off
    hotels_to_add = [
        HotelCreateOrUpdateSchema(**hotel)
        for hotel in hotels_data
    ]
    rooms_to_add = [
        RoomCreateSchema(**room)
        for room in rooms_data
    ]
    # fmt: on
    await db.hotels.add_bulk(hotels_to_add)
    await db.rooms.add_bulk(rooms_to_add)
    await db.commit()
