from pydantic import BaseModel


class SFriendRequest(BaseModel):
    user_sended_id: int

    