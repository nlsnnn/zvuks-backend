from fastapi import status
from app.friends.dao import FriendsDAO
from app.friends.exceptions import FriendsException
from app.friends.models import FriendStatus
from app.users.dao import UsersDAO
from app.users.service import UserService


class FriendRequestService:
    @staticmethod
    async def send_friend_request(user_sended_id: int, user_received_id: int):
        if user_received_id == user_sended_id:
            raise FriendsException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Нельзя добавить в друзья самого себя",
            )

        friendship = await FriendsDAO.get_friendship(user_received_id, user_sended_id)
        if friendship:
            if friendship.status == FriendStatus.deleted:
                return await FriendsDAO.update(
                    filter_by={"id": friendship.id}, status=FriendStatus.pending
                )
            elif friendship.status in (FriendStatus.pending, FriendStatus.friends):
                raise FriendsException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Уже отправлена заявка в друзья",
                )

        users = await UsersDAO.find_all_by_ids([user_received_id, user_sended_id])
        if len(users) != 2:
            raise FriendsException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Пользователи не найдены",
            )

        return await FriendsDAO.add(
            user_sended_id=user_sended_id,
            user_received_id=user_received_id,
            status=FriendStatus.pending,
        )

    @staticmethod
    async def accept_friend_request(user_sended_id: int, user_received_id: int):
        return await FriendsDAO.update(
            filter_by={
                "user_sended_id": user_sended_id,
                "user_received_id": user_received_id,
            },
            status=FriendStatus.friends,
        )

    @staticmethod
    async def reject_friend_request(user_sended_id: int, user_received_id: int):
        friendship = await FriendsDAO.get_friendship(user_sended_id, user_received_id)
        return await FriendsDAO.delete(id=friendship.id)

    @staticmethod
    async def delete_friend(f_user_id: int, s_user_id: int):
        friendship = await FriendsDAO.get_friendship(f_user_id, s_user_id)
        return await FriendsDAO.update(
            filter_by={"id": friendship.id}, status=FriendStatus.deleted
        )

    async def _get_requests(user_id: int, field: str):
        requests = await FriendsDAO.find_all(
            **{field: user_id}, status=FriendStatus.pending
        )
        user_ids = [
            request.user_sended_id
            if field == "user_received_id"
            else request.user_received_id
            for request in requests
        ]
        users = await UsersDAO.find_all_by_ids(user_ids)
        data = UserService.get_users_dto(users)
        return data

    # Получение пользователей которые отправили заявку в друзья пользователю
    @staticmethod
    async def get_pending_requests(user_id: int):
        return await FriendRequestService._get_requests(user_id, "user_received_id")

    # Получение пользователей которым пользователь отправил заявку в друзья
    @staticmethod
    async def get_sended_requests(user_id: int):
        return await FriendRequestService._get_requests(user_id, "user_sended_id")

    @staticmethod
    async def get_friends(user_id: int):
        friends_ids = await FriendsDAO.get_all_friends_id(user_id)
        if not friends_ids:
            return []

        users = await UsersDAO.find_all_by_ids(friends_ids)
        data = UserService.get_users_dto(users)
        return data
