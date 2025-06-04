import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class DatabaseSettings(BaseModel):
    NAME: str = os.getenv(
        "POSTGRES_DB",
        "booking",
    )
    USER: str = os.getenv(
        "POSTGRES_USER",
        "admin",
    )
    PASS: str = os.getenv(
        "POSTGRES_PASSWORD",
        "admin",
    )
    HOST: str = os.getenv(
        "DB_HOST",
        "localhost",
    )
    PORT: int = os.getenv(
        "DB_PORT",
        5433,
    )
    URL: PostgresDsn = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"


class JWTSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "src" / "certs" / "jwt" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "src" / "certs" / "jwt" / "public.pem"

    ACCESS_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(days=30)
    ALGORITHM: str = "RS256"
    TOKEN_TYPE: str = "Bearer"
    TOKEN_OWNER: str = "booking"

    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    TOKEN_TYPE_FIELD: str = "type"


class ModelsSettings(BaseModel):
    DECIMAL_PRECISION: int = 10
    DECIMAL_SCALE: int = 2


class PaginationSettings(BaseModel):
    MAX_ENTITIES_PER_PAGE: int = 100


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    models: ModelsSettings = ModelsSettings()
    pagination: PaginationSettings = PaginationSettings()


settings = Settings()
