from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageCreate, MessageEdit, MessageRead, MessagePublish
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.chat.websocket import WebSocketManager, get_websocket_manager
from app.users.service import UserService
from app.connections.nats import NatsClient
from app.services.nats import NatsService

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
    messages_dto = [
        MessageRead(
            id=msg.id,
            sender=msg.sender_id,
            recipient=msg.recipient_id,
            content=msg.content,
            created=str(msg.created_at),
            updated=msg.created_at < msg.updated_at,
        )
        for msg in messages
    ]

    user = await UsersDAO.find_one_or_none(**{"id": user_id})
    user_dto = UserService.get_user_dto(user)
    return {"user": user_dto, "messages": messages_dto}


@router.post("/messages", response_model=MessageCreate)
async def send_message(
    message: MessageCreate,
    user_data: User = Depends(get_current_user),
    manager: WebSocketManager = Depends(get_websocket_manager),
):
    message_orm = await MessagesDAO.add(
        sender_id=user_data.id,
        recipient_id=message.recipient,
        content=message.content,
    )
    message_data = MessageRead(
        id=message_orm.id,
        sender=user_data.id,
        recipient=message.recipient,
        content=message.content,
        created=str(message_orm.created_at),
        updated=message_orm.created_at < message_orm.updated_at,
        type="message",
    )

    await manager.notify_user(user_data.id, message_data.model_dump())
    await manager.notify_user(message.recipient, message_data.model_dump())

    nats_js = await NatsClient.get_jetstream()
    await NatsService.publish_message_ai(
        nats_js,
        message_data=MessagePublish(
            text=message_data.content,
            message_id=message_data.id,
            user_id=message_data.sender,
        ),
    )

    return {
        "recipient": message.recipient,
        "content": message.content,
        "msg": "Сообщение сохранено",
    }


@router.put("/messages")
async def edit_message(
    message_data: MessageEdit,
    user_data: User = Depends(get_current_user),
    manager: WebSocketManager = Depends(get_websocket_manager),
):
    message = await MessagesDAO.find_one_or_none_by_id(message_data.id)
    if not message:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")

    await MessagesDAO.update(
        filter_by={"id": message_data.id}, content=message_data.content
    )

    data = {
        "id": message.id,
        "content": message_data.content,
        "type": "update",
    }

    await manager.notify_user(message.sender_id, data)
    await manager.notify_user(message.recipient_id, data)

    return {"msg": "Сообщение обновлено"}


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    user_data: User = Depends(get_current_user),
    manager: WebSocketManager = Depends(get_websocket_manager),
):
    message = await MessagesDAO.find_one_or_none_by_id(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")

    await MessagesDAO.delete(id=message_id)

    data = {
        "id": message_id,
        "type": "delete",
    }

    await manager.notify_user(message.sender_id, data)
    await manager.notify_user(message.recipient_id, data)

    return {"msg": "Сообщение удалено"}
