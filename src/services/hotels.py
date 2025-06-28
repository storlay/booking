from datetime import date

from src.api.v1.utils import get_hotels_filters_from_params
from src.exceptions.api.hotels import HotelNotFoundHTTPException
from src.exceptions.repository.hotels import ObjectNotFoundRepoException
from src.schemas.hotels import HotelCreateOrUpdateSchema
from src.schemas.hotels import HotelSchema
from src.schemas.hotels import HotelsQueryParamsSchema
from src.schemas.hotels import PartialUpdateHotelSchema
from src.schemas.pagination import PaginationSchema
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        filter_params: HotelsQueryParamsSchema,
        pagination_params: PaginationSchema,
    ) -> list[HotelSchema]:
        filters = get_hotels_filters_from_params(filter_params)
        return await self.db.hotels.get_filtered(
            pagination_params.limit,
            pagination_params.offset,
            None,
            *filters,
        )

    async def get_available_hotels(
        self,
        date_from: date,
        date_to: date,
        filter_params: HotelsQueryParamsSchema,
        pagination_params: PaginationSchema,
    ) -> list[HotelSchema]:
        filters = get_hotels_filters_from_params(filter_params)
        return await self.db.hotels.get_with_available_rooms(
            date_from,
            date_to,
            pagination_params.limit,
            pagination_params.offset,
            filters,
        )

    async def get_hotel(
        self,
        hotel_id: int,
    ) -> HotelSchema:
        try:
            return await self.db.hotels.get_one(
                id=hotel_id,
            )
        except ObjectNotFoundRepoException:
            raise HotelNotFoundHTTPException

    async def add_hotel(
        self,
        data: HotelCreateOrUpdateSchema,
    ) -> HotelSchema:
        result = await self.db.hotels.add(data)
        await self.db.commit()
        return result

    async def update_hotel(
        self,
        hotel_id: int,
        data: HotelCreateOrUpdateSchema,
    ) -> None:
        try:
            await self.db.hotels.update_one(
                data,
                id=hotel_id,
            )
            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise HotelNotFoundHTTPException

    async def update_hotel_partial(
        self,
        data: PartialUpdateHotelSchema,
        hotel_id: int,
    ) -> None:
        try:
            await self.db.hotels.update_one(
                data,
                partially=True,
                id=hotel_id,
            )
            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise HotelNotFoundHTTPException

    async def delete_hotel(self, hotel_id: int) -> None:
        try:
            await self.db.hotels.delete_one(
                id=hotel_id,
            )
            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise HotelNotFoundHTTPException
