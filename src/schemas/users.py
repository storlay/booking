from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=200,
    )

    @field_validator(
        "email",
        mode="after",
    )
    @classmethod
    def email_to_lower(cls, value: str) -> str:
        return value.lower()


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
