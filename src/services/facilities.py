from src.exceptions.api.facilities import FacilityAlreadyExistsHTTPException
from src.exceptions.repository.hotels import CannotAddObjectRepoException
from src.schemas.facilities import FacilityCreateSchema
from src.schemas.facilities import FacilitySchema
from src.schemas.pagination import PaginationSchema
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_all_facilities(
        self,
        pagination: PaginationSchema,
    ) -> list[FacilitySchema]:
        return await self.db.facilities.get_all(
            pagination.limit,
            pagination.offset,
        )

    async def create_facility(
        self,
        data: FacilityCreateSchema,
    ):
        try:
            facility = await self.db.facilities.add(data)
            await self.db.commit()
            return facility
        except CannotAddObjectRepoException:
            raise FacilityAlreadyExistsHTTPException
