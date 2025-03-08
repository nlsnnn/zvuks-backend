import asyncio
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageCreate, MessageRead
from app.users.dao import UsersDAO
from app.users.dependencies import token_depends
from app.users.models import User


router = APIRouter(prefix="/chat", tags=["Chat"])


active_connections: Dict[int, WebSocket] = {}


async def notify_user(user_id: int, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)


@router.get("/messages/{user_id}")
async def get_messages(user_id: int, user_data: User = Depends(token_depends.get_current_user)):
    return await MessagesDAO.get_messages_between_users(
        f_user_id=user_id,
        s_user_id=user_data.id
    ) or []


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, user_data: User = Depends(token_depends.get_current_user)):
    message_orm = await MessagesDAO.add(
        sender_id=user_data.id,
        recipient_id=message.recipient_id,
        content=message.content
    )
    message_data = {
        'sender_id': user_data.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
        'created_at': str(message_orm.created_at)
    }
    await notify_user(user_data.id, message_data)
    await notify_user(message.recipient_id, message_data)

    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}