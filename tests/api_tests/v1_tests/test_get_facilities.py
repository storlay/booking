from fastapi import status


async def test_get_facilities(
    ac,
    populate_db,
):
    response = await ac.get("/v1/facilities")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
