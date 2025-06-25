import pytest
from fastapi import status


@pytest.mark.parametrize(
    "email, password",
    [
        ("user@example.com", "0" * 8),
        ("my@mail.com", "2" * 10),
    ],
)
async def test_auth_flow(
    email,
    password,
    ac,
):
    register_body = {
        "email": email,
        "password": password,
    }
    register_response = await ac.post(
        "/v1/auth/register",
        json=register_body,
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    register_response_data = register_response.json()
    assert isinstance(register_response_data, dict)
    assert register_response_data["status"] == "ok"

    login_body = register_body.copy()
    login_response = await ac.post(
        "/v1/auth/login",
        json=login_body,
    )
    assert login_response.status_code == status.HTTP_200_OK
    login_response_data = login_response.json()
    assert isinstance(login_response_data, dict)
    assert login_response_data["access"]
    assert login_response_data["refresh"]
    assert login_response_data["token_type"]

    ac.headers.update(
        {
            "Authorization": f"Bearer {login_response_data['refresh']}",
        }
    )

    refresh_response = await ac.post(
        "/v1/auth/refresh",
    )
    assert refresh_response.status_code == status.HTTP_200_OK
    refresh_response_data = refresh_response.json()
    assert isinstance(refresh_response_data, dict)
    assert refresh_response_data["access"]

    ac.headers.update(
        {
            "Authorization": f"Bearer {refresh_response_data['access']}",
        }
    )

    me_response = await ac.get(
        "/v1/auth/me",
    )
    assert me_response.status_code == status.HTTP_200_OK
    me_response_data = me_response.json()
    assert isinstance(me_response_data, dict)
    assert me_response_data["id"]
    assert me_response_data["email"] == email
    assert "first_name" in me_response_data
    assert "last_name" in me_response_data
