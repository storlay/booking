from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
