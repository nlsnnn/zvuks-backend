from typing import List
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserProfile, SUserRead


class UserService:
    @staticmethod
    def get_user_dto(user_data: User):
        return SUserRead(
            id=user_data.id, username=user_data.username, avatar=user_data.avatar_path
        )

    @staticmethod
    def get_users_dto(users: List[User]):
        data = [
            SUserRead(id=user.id, username=user.username, avatar=user.avatar_path)
            for user in users
        ]
        return data

    @staticmethod
    async def get_profile(user_data: User):
        return UserService.get_user_dto(user_data)
