import os

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


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
    SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
    )
    ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class ModelsSettings(BaseModel):
    DECIMAL_PRECISION: int = 10
    DECIMAL_SCALE: int = 2


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    models: ModelsSettings = ModelsSettings()


settings = Settings()
