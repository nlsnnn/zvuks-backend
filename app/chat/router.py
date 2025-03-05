from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageCreate, MessageRead
from app.users.dao import UsersDAO
from app.users.dependencies import token_depends
from app.users.models import User


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/messages/{user_id}")
async def get_messages(user_id: int, user_data: User = Depends(token_depends.get_current_user)):
    return await MessagesDAO.get_messages_between_users(
        f_user_id=user_id,
        s_user_id=user_data.id
    ) or []


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, user_data: User = Depends(token_depends.get_current_user)):
    await MessagesDAO.add(
        sender_id=user_data.id,
        recipient_id=message.recipient_id,
        content=message.content
    )

    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}