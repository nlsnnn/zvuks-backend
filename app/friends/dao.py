from app.dao.base import BaseDAO
from app.friends.models import Friend


class FriendsDAO(BaseDAO):
    model = Friend