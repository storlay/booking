from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )
