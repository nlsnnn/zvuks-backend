from typing import List
from app.services.utils import Utils
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserProfile, SUserRead, SUserUpdate


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

    @staticmethod
    async def update_user(data: SUserUpdate, user: User):
        if data.avatar:
            path = await UserService.save_avatar(data.avatar, user)
            await UsersDAO.update(filter_by={"id": user.id}, avatar_path=path)

        user_updated = await UsersDAO.find_one_or_none_by_id(user.id)
        user_dto = UserService.get_user_dto(user_updated)
        return user_dto

    @staticmethod
    async def save_avatar(file, user: User):
        directory = UserService.get_directory_name(user)
        path = await Utils.upload_file(file, directory, ["png", "jpg", "jpeg"])
        return path

    @staticmethod
    def get_directory_name(user: User):
        return f"avatars/{user.id}"
