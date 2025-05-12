import pytest
from httpx import Response
from app.users.dao import UsersDAO
from app.users import router

REGISTER_URL = "/auth/register/"


class DummyUser:
    def __init__(self, id=1):
        self.id = id


@pytest.mark.asyncio
async def test_register_conflict(async_client, monkeypatch):
    async def fake_find_one_or_none(email):
        return DummyUser()

    monkeypatch.setattr(UsersDAO, "find_one_or_none", fake_find_one_or_none)

    payload = {"email": "a@a.ru", "username": "aaaaa", "password": "secret"}
    response = await async_client.post(url=REGISTER_URL, json=payload)
    assert response.status_code == 409
    assert "Пользователь уже существует" in response.text


@pytest.mark.asyncio
async def test_register_success(async_client, monkeypatch):
    async def fake_find_one_or_none(email):
        return None

    called = {}

    async def fake_add(**kwargs):
        called.update(kwargs)
        return DummyUser(id=123)

    monkeypatch.setattr(UsersDAO, "find_one_or_none", fake_find_one_or_none)
    monkeypatch.setattr(UsersDAO, "add", fake_add)

    payload = {"email": "a@a.ru", "username": "aaaaa", "password": "secret"}
    response = await async_client.post(url=REGISTER_URL, json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "success"}
    assert called["email"] == "a@a.ru"
    assert "password" in called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fake_result, expected_status, expect_token",
    [
        ("Неверный пароль", 401, False),
        ("Пользователя не существует", 401, False),
        (DummyUser(123), 200, True),
    ],
)
async def test_login(
    async_client, monkeypatch, fake_result, expected_status, expect_token
):
    async def fake_authenticate_user(identifier, password):
        return fake_result

    monkeypatch.setattr(router, "authenticate_user", fake_authenticate_user)

    payload = {"identifier": "a@a.ru", "password": "secret"}
    response: Response = await async_client.post(url="/auth/login/", json=payload)
    assert response.status_code == expected_status
    if expect_token:
        data = response.json()
        assert "access_token" in data
        assert data["access_token"].count(".") == 2
    else:
        assert fake_result in response.text
