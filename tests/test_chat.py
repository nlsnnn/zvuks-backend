import pytest
from datetime import datetime
from fastapi import Request
from httpx import Response
from app.chat.dao import MessagesDAO
from app.main import app
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user


class DummyUser:
    def __init__(self, id=1, username="User", avatar="path"):
        self.id = id
        self.username = username
        self.avatar_path = avatar


class DummyMsg:
    def __init__(self, id, sender_id, recipient_id, content, created_at, updated_at):
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at


@pytest.fixture(autouse=True)
def override_user():
    async def fake_current_user(request: Request):
        return DummyUser(id=14)

    app.dependency_overrides[get_current_user] = fake_current_user
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_messages_empty(async_client, monkeypatch):
    async def fake_get_msgs(f_user_id, s_user_id):
        assert f_user_id == 7
        assert s_user_id == 14
        return []

    async def fake_find_user(**kwargs):
        assert kwargs["id"] == 7
        return DummyUser(id=7)

    monkeypatch.setattr(MessagesDAO, "get_messages_between_users", fake_get_msgs)
    monkeypatch.setattr(UsersDAO, "find_one_or_none", fake_find_user)

    response: Response = await async_client.get("/chat/messages/7")
    assert response.status_code == 200, f"{response.status_code} / {response.text}"
    body = response.json()
    assert body["user"]["id"] == 7
    assert body["messages"] == []


@pytest.mark.asyncio
async def test_get_messages_with_data(async_client, monkeypatch):
    ts = datetime(2025, 5, 12, 0, 0)
    fake_msg = DummyMsg(
        id=1,
        sender_id=14,
        recipient_id=7,
        content="hello",
        created_at=ts,
        updated_at=ts,
    )

    async def fake_get_msgs(f_user_id, s_user_id):
        return [fake_msg]

    async def fake_find_user(**kwargs):
        return DummyUser(id=7)

    monkeypatch.setattr(MessagesDAO, "get_messages_between_users", fake_get_msgs)
    monkeypatch.setattr(UsersDAO, "find_one_or_none", fake_find_user)

    response: Response = await async_client.get("/chat/messages/7")
    assert response.status_code == 200, f"{response.status_code} / {response.text}"
    data = response.json()["messages"][0]
    assert data["id"] == 1
    assert data["sender"] == 14
    assert data["recipient"] == 7
    assert data["content"] == "hello"
    assert data["updated"] is False
