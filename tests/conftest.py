import pytest

from src.config import settings
from src.db.database import Base
from src.db.database import async_engine_null_pull


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    assert settings.app.MODE == "TEST"

    async with async_engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
