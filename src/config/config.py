import os
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic import computed_field
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


class RedisSettings(BaseModel):
    HOST: str = os.getenv("REDIS_HOST")
    PORT: int = os.getenv("REDIS_PORT")

    @computed_field
    @property
    def URL(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}"


class ModelsSettings(BaseModel):
    DECIMAL_PRECISION: int = 10
    DECIMAL_SCALE: int = 2

    DEFAULT_IMAGE_PATH: Path = BASE_DIR / "src" / "static" / "images"
    DEFAULT_IMAGE_SIZES: list[int] = [1000, 500, 300]

    @computed_field
    @property
    def MAX_DECIMAL_VALUE(self) -> Decimal:
        digits_before_decimal = self.DECIMAL_PRECISION - self.DECIMAL_SCALE
        max_value_str = "9" * digits_before_decimal + "." + "9" * self.DECIMAL_SCALE
        return Decimal(max_value_str)


class PaginationSettings(BaseModel):
    MAX_ENTITIES_PER_PAGE: int = 100


class AppSettings(BaseModel):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = os.getenv("APP_MODE")


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    models: ModelsSettings = ModelsSettings()
    pagination: PaginationSettings = PaginationSettings()
    redis: RedisSettings = RedisSettings()
    app: AppSettings = AppSettings()
