from typing import Annotated

from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import field_validator

from src.schemas.base import IntegerId


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        MinLen(8),
        MaxLen(200),
    ]

    @field_validator(
        "email",
        mode="after",
    )
    @classmethod
    def email_to_lower(cls, value: str) -> str:
        return value.lower()


class UserSchema(BaseModel):
    id: IntegerId
    email: EmailStr
    first_name: str | None
    last_name: str | None


class UserWithPasswordSchema(UserSchema):
    password: bytes

    model_config = ConfigDict(
        from_attributes=True,
    )

    @field_validator(
        "password",
        mode="before",
    )
    @classmethod
    def password_to_bytes(cls, value: str) -> bytes:
        return value.encode("utf-8")
