from typing import Optional
from pydantic import BaseModel, Field


class SFriendRequest(BaseModel):
    user_sended_id: Optional[int] = Field(default=None)
    user_received_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)