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
from src.schemas.users import UserAuthSchema
from src.services.auth import AuthService
from src.utils.transaction import TransactionManager
from tests.utils import get_mock_data_from_file


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


@pytest.fixture
async def db(prepare_db):
    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        yield transaction


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
    for user in users_to_add:
        user.password = AuthService.hash_password(user.password).decode("utf-8")

    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        await transaction.users.add_bulk(users_to_add)
        await transaction.hotels.add_bulk(hotels_to_add)
        await transaction.rooms.add_bulk(rooms_to_add)
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
