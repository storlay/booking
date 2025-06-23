from unittest import mock

import pytest
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependecies.db import get_db_transaction
from src.config import settings
from src.db.database import Base
from src.db.database import async_engine_null_pull
from src.db.database import async_session_null_pool
from src.main import app
from src.schemas.facilities import FacilityCreateSchema
from src.schemas.hotels import HotelCreateOrUpdateSchema
from src.schemas.rooms import RoomCreateSchema
from src.schemas.users import UserAuthSchema
from src.services.auth import AuthService
from src.utils.transaction import TransactionManager
from tests.utils import get_mock_data_from_file


async def get_test_db():
    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        yield transaction


app.dependency_overrides[get_db_transaction] = get_test_db


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.app.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def prepare_db(check_test_mode):
    async with async_engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def auth_user_data():
    return {
        "email": "kot@pes.com",
        "password": "12345678",
    }


@pytest.fixture(scope="session", autouse=True)
async def register_user(
    prepare_db,
    ac,
    auth_user_data,
):
    await ac.post(
        "/v1/auth/register",
        json=auth_user_data,
    )


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def user_ac(
    register_user,
    auth_user_data,
    ac,
):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.post(
            "/v1/auth/login",
            json=auth_user_data,
        )
        assert response.status_code == status.HTTP_200_OK
        ac.headers.update(
            {
                "Authorization": f"Bearer {response.json()['access']}",
            }
        )
        yield ac


@pytest.fixture
async def db(prepare_db):
    async for db in get_test_db():
        yield db


@pytest.fixture(scope="session")
async def populate_db():
    hotels_to_add = await get_mock_data_from_file(
        "tests/mock_hotels.json",
        HotelCreateOrUpdateSchema,
    )
    rooms_to_add = await get_mock_data_from_file(
        "tests/mock_rooms.json",
        RoomCreateSchema,
    )
    users_to_add = await get_mock_data_from_file(
        "tests/mock_users.json",
        UserAuthSchema,
    )
    facilities_to_add = await get_mock_data_from_file(
        "tests/mock_facilities.json",
        FacilityCreateSchema,
    )
    for user in users_to_add:
        user.password = AuthService.hash_password(user.password).decode("utf-8")

    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        await transaction.users.add_bulk(users_to_add)
        await transaction.hotels.add_bulk(hotels_to_add)
        await transaction.rooms.add_bulk(rooms_to_add)
        await transaction.facilities.add_bulk(facilities_to_add)
        await transaction.commit()


@pytest.fixture
async def users_list(
    populate_db,
    db,
):
    return await db.users.get_all(
        limit=10,
        offset=0,
    )


@pytest.fixture
async def rooms_list(
    populate_db,
    db,
):
    return await db.rooms.get_all(
        limit=10,
        offset=0,
    )


@pytest.fixture
async def user(users_list):
    return users_list[0]


@pytest.fixture
async def room(rooms_list):
    return rooms_list[0]
