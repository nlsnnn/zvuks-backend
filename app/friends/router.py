from fastapi import APIRouter, Depends

from app.friends.dao import FriendsDAO
from app.friends.models import FriendStatus
from app.users.models import User
from app.users.dependencies import TokenDepends


router = APIRouter(prefix='/friends', tags=['Friends'])

token_depends = TokenDepends()


@router.post('/')
async def create_friends(
    user_received: int,
    user_data: User = Depends(token_depends.get_current_user)
):
    await FriendsDAO.add(
        user_sended_id=user_data.id,
        user_received_id=user_received
    )

    return {'message': 'Friend request sent!'}


@router.get('/')
async def get_friends():
    return await FriendsDAO.find_all(status=FriendStatus.friends)
    

@router.get('/pending-users')
async def get_my_pending_users(
    user_data: User = Depends(token_depends.get_current_user)
):
    users = await FriendsDAO.find_all(
        user_received_id=user_data.id
    )

    return {'users': users}


@router.get('/pending-requests')
async def get_my_pending_requests(
    user_data: User = Depends(token_depends.get_current_user)
):
    users = await FriendsDAO.find_all(
        user_sended_id=user_data.id
    )

    return {'users': users}


@router.put('/')
async def update_friends(
    status: FriendStatus,
    user_sended_id: int,
    user_received_id: int
):
    data = await FriendsDAO.update(
        filter_by={user_received_id: user_received_id},
        user_received_id=user_received_id,
        user_sended_id=user_sended_id,
        status=status
    )
    return {'data': data}


@router.put('/update-sended')
async def update_sended_friends(
    status: FriendStatus,
    user_id: int,
    user_data: User = Depends(token_depends.get_current_user),
):
    data = await FriendsDAO.update(
        user_received_id=user_id,
        user_sended_id=user_data.id,
        status=status
    )
    return {'data': data}
