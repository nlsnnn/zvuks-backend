from typing import Optional
from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int
    sender: int
    recipient: int
    content: str
    created: str
    updated: bool
    type: Optional[str] = Field(default=None)


class MessageCreate(BaseModel):
    recipient: int
    content: str


class MessageEdit(BaseModel):
    id: int
    content: str
