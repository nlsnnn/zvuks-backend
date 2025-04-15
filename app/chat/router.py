from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageCreate
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.chat.websocket import WebSocketManager, get_websocket_manager
from app.users.service import UserService


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    maganer: WebSocketManager = Depends(get_websocket_manager),
):
    await websocket.accept()
    await maganer.add_connection(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await maganer.remove_connection(user_id)
    finally:
        await maganer.remove_connection(user_id)


@router.get("/messages/{user_id}")
async def get_messages(user_id: int, user_data: User = Depends(get_current_user)):
    messages = await MessagesDAO.get_messages_between_users(
        f_user_id=user_id, s_user_id=user_data.id
    )

    user = await UsersDAO.find_one_or_none(**{"id": user_id})
    user_dto = UserService.get_user_dto(user)
    return {"user": user_dto, "messages": messages}


@router.post("/messages", response_model=MessageCreate)
async def send_message(
    message: MessageCreate,
    user_data: User = Depends(get_current_user),
    manager: WebSocketManager = Depends(get_websocket_manager),
):
    message_orm = await MessagesDAO.add(
        sender_id=user_data.id,
        recipient_id=message.recipient_id,
        content=message.content,
    )
    message_data = {
        "sender_id": user_data.id,
        "recipient_id": message.recipient_id,
        "content": message.content,
        "created_at": str(message_orm.created_at),
    }

    await manager.notify_user(user_data.id, message_data)
    await manager.notify_user(message.recipient_id, message_data)

    return {
        "recipient_id": message.recipient_id,
        "content": message.content,
        "status": "ok",
        "msg": "Message saved!",
    }
