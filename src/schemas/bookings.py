from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator
from pydantic import model_validator

from src.schemas.base import PositiveDecimal


class BookingCreateRequestSchema(BaseModel):
    date_from: date
    date_to: date
    room_id: int

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


class BookingCreateSchema(BookingCreateRequestSchema):
    user_id: int
    price: PositiveDecimal


class BookingSchema(BookingCreateSchema):
    model_config = ConfigDict(
        from_attributes=True,
    )
