from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=200,
    )


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
