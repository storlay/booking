from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import model_validator

from src.schemas.base import IntegerId
from src.schemas.base import PositiveDecimal


class BookingCreateSchema(BaseModel):
    user_id: IntegerId
    price: PositiveDecimal
    date_from: date
    date_to: date
    room_id: IntegerId


class BookingSchema(BookingCreateSchema):
    id: IntegerId
    created_at: datetime


class BookingCreateRequestSchema(BaseModel):
    date_from: date
    date_to: date
    room_id: IntegerId

    @field_validator(
        "date_from",
        mode="after",
    )
    @classmethod
    def validate_date_from(cls, value: date):
        if value < date.today():
            raise ValueError("`date_from` cannot be earlier than the current date")
        return value

    @model_validator(mode="after")
    def validate_date_to(self):
        if self.date_from > self.date_to:
            raise ValueError("`date_from` cannot be earlier than `date_to`")
        return self


class BookingUpdateSchema(BaseModel):
    date_from: date
    date_to: date
