


from app.friends.dao import FriendsDAO
from app.friends.models import FriendStatus
from app.users.dao import UsersDAO


class FriendRequestService:
    @staticmethod
    async def send_friend_request(user_sended_id: int, user_received_id: int):
        return await FriendsDAO.add(
            user_sended_id=user_sended_id,
            user_received_id=user_received_id,
            status=FriendStatus.pending
        )
    
    @staticmethod
    async def accept_friend_request(user_sended_id: int, user_received_id: int):
        return await FriendsDAO.update(
            filter_by={
                "user_sended_id": user_sended_id,
                "user_received_id": user_received_id
            },
            status=FriendStatus.friends
        )
    
    @staticmethod
    async def reject_friend_request(user_sended_id: int, user_received_id: int):
        return await FriendsDAO.delete(
            user_sended_id=user_sended_id,
            user_received_id=user_received_id
        )
    

    # Получение пользователей которые отправили заявку в друзья пользователю
    @staticmethod
    async def get_pending_requests(user_id: int):
        return await FriendsDAO.find_all(
            user_received_id=user_id,
            status=FriendStatus.pending
        )
    

    # Получение пользователей которым пользователь отправил заявку в друзья 
    @staticmethod
    async def get_sended_requests(user_id: int):
        return await FriendsDAO.find_all(
            user_sended_id=user_id,
            status=FriendStatus.pending
        )
    

    @staticmethod
    async def get_friends(user_id: int):
        friends_ids = await FriendsDAO.get_all_friends_id(user_id)
        users = []
        for user_id in friends_ids:
            user = await UsersDAO.find_one_or_none_by_id(user_id)
            users.append(user)
        
        return users