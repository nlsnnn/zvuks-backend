from app.users.dao import UsersDAO
from app.users.schemas import SUserProfile


class UserService:
    @staticmethod
    async def get_profile(user_id: int):
        user = await UsersDAO.find_one_or_none_by_id(user_id)

        return SUserProfile(
            id=user.id,
            username=user.username
        )