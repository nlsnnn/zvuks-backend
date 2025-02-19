from fastapi import APIRouter, Depends

from app.friends.schemas import SFriendRequest
from app.friends.service import FriendRequestService
from app.users.models import User
from app.users.dependencies import TokenDepends


router = APIRouter(prefix='/friends', tags=['Friends'])

token_depends = TokenDepends()


@router.get('/')
async def get_friends(
    user_data: User = Depends(token_depends.get_current_user)
):
    print(f'{user_data=}')
    friends = await FriendRequestService.get_friends(user_data.id)
    return {'friends': friends}


@router.get('/pending')
async def get_pending_requests(
    user_data: User = Depends(token_depends.get_current_user)
):
    requests = await FriendRequestService.get_pending_requests(user_data.id)
    return {'requests': requests}


@router.get('/sended')
async def get_sended_requests(
    user_data: User = Depends(token_depends.get_current_user)
):
    requests = await FriendRequestService.get_sended_requests(user_data.id)
    return {'requests': requests}


@router.post('/')
async def send_friend_request(
    user_received_id: int,
    user_data: User = Depends(token_depends.get_current_user)
):
    await FriendRequestService.send_friend_request(
        user_sended_id=user_data.id,
        user_received_id=user_received_id
    )
    return {'message': 'Friend request sent!'}


@router.post('/accept')
async def accept_friend_request(
    request: SFriendRequest,
    user_data: User = Depends(token_depends.get_current_user)
):
    await FriendRequestService.accept_friend_request(
        request.user_sended_id,
        user_data.id
    )
    return {'message': 'Friend request accepted'}


@router.post('/reject')
async def reject_friend_request(
    request: SFriendRequest,
    user_data: User = Depends(token_depends.get_current_user)
):
    await FriendRequestService.reject_friend_request(
        user_sended_id=request.user_sended_id,
        user_received_id=user_data.id
    )


@router.post('/delete')
async def delete_friend(
    request: SFriendRequest,
    user_data: User = Depends(token_depends.get_current_user)
):
    await FriendRequestService.delete_friend(
        request.user_sended_id,
        user_data.id
    )
    return {'message': 'Friend deleted'}