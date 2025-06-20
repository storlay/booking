from fastapi import status


async def test_get_available_hotels(
    ac,
    populate_db,
):
    response = await ac.get(
        "/v1/hotels/available",
        params={
            "date_from": "2025-06-01",
            "date_to": "2025-06-10",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
