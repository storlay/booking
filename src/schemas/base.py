from pydantic import BaseModel


class BaseSuccessResponseSchema(BaseModel):
    status: str = "ok"
