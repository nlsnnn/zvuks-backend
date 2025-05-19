from fastapi import APIRouter

from app.friends.schemas import SFriendRequest
from app.friends.service import FriendRequestService
from app.users.dependencies import CurrentUserDep


router = APIRouter(prefix="/friends", tags=["Friends"])


@router.get("/")
async def get_friends(user_data: CurrentUserDep):
    friends = await FriendRequestService.get_friends(user_data.id)
    return {"friends": friends}


@router.get("/pending")
async def get_pending_requests(user_data: CurrentUserDep):
    requests = await FriendRequestService.get_pending_requests(user_data.id)
    return {"requests": requests}


@router.get("/sended")
async def get_sended_requests(user_data: CurrentUserDep):
    requests = await FriendRequestService.get_sended_requests(user_data.id)
    return {"requests": requests}


@router.post("/")
async def send_friend_request(
    data: SFriendRequest, user_data: CurrentUserDep
):
    await FriendRequestService.send_friend_request(
        user_sended_id=user_data.id, user_received_id=data.user_received_id
    )

    return {"message": "Запрос отправлен"}


@router.post("/accept")
async def accept_friend_request(
    request: SFriendRequest, user_data: CurrentUserDep
):
    await FriendRequestService.accept_friend_request(
        request.user_sended_id, user_data.id
    )
    return {"message": "Запрос принят"}


@router.post("/reject")
async def reject_friend_request(
    request: SFriendRequest, user_data: CurrentUserDep
):
    await FriendRequestService.reject_friend_request(
        user_sended_id=request.user_sended_id, user_received_id=user_data.id
    )
    return {"message": "Дружба отклонена"}


@router.post("/delete")
async def delete_friend(
    request: SFriendRequest, user_data: CurrentUserDep
):
    await FriendRequestService.delete_friend(request.user_id, user_data.id)
    return {"message": "Друг удален"}
