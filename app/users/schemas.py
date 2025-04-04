from typing import Optional
from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )
    username: str = Field(
        min_length=3, max_length=50, description="Имя пользователя, от 3 до 50 символов"
    )


class SUserAuth(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class SUserUpdate(BaseModel):
    avatar: Optional[UploadFile] = Form(default=None)

    @classmethod
    async def as_form(
        cls,
        avatar: Optional[UploadFile] 
    ):
        return cls(
            avatar=avatar
        )



class SUserRead(BaseModel):
    id: int
    username: str
    avatar: str


class SUserProfile(SUserRead):
    pass


