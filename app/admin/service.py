from fastapi import status

from app.music.album.dao import AlbumDAO
from app.music.song.dao import SongDAO
from app.users.dao import UsersDAO
from app.users.models import User
from app.admin.exceptions import AdminException


class AdminService:
    @staticmethod
    async def block_user(user_id: int, current_user: User):
        if user_id == current_user.id:
            raise AdminException(
                message="Нельзя заблокировать самого себя",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        user = await UsersDAO.find_one_or_none_by_id(user_id)
        if not user:
            raise AdminException(
                message="Пользователя не существует",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if user.is_admin:
            raise AdminException(
                message="Пользователь является админом",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if not user.is_user:
            raise AdminException(
                message="Пользователь уже заблокирован",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        await UsersDAO.update(filter_by={"id": user_id}, is_user=False)
        await SongDAO.update(filter_by={"user_id": user_id}, is_archive=True)
        await AlbumDAO.update(filter_by={"user_id": user_id}, is_archive=True)

    @staticmethod
    async def unblock_user(user_id: int, current_user: User):
        if user_id == current_user.id:
            raise AdminException(
                message="Нельзя раззаблокировать самого себя",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        user = await UsersDAO.find_one_or_none_by_id(user_id)
        if not user:
            raise AdminException(
                message="Пользователя не существует",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if user.is_user:
            raise AdminException(
                message="Пользователь не заблокирован",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        await UsersDAO.update(filter_by={"id": user_id}, is_user=True)
        await SongDAO.update(filter_by={"user_id": user_id}, is_archive=False)
        await AlbumDAO.update(filter_by={"user_id": user_id}, is_archive=False)
