from fastapi import status

from src.schemas.facilities import FacilityCreateSchema


async def test_add_facility(ac):
    data_to_add = FacilityCreateSchema(
        title="Security 24/7",
    )
    response = await ac.post(
        "/v1/facilities",
        json=data_to_add.model_dump(),
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert response_data["title"] == data_to_add.title
