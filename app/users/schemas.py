from typing import Optional, Union
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
    identifier: Union[str, EmailStr] = Field(
        description="Электронная почта или имя пользователя"
    )
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class SUserAuthResponse(BaseModel):
    access_token: str = Field(serialization_alias="accessToken")
    refresh_token: Optional[str] = Field(
        serialization_alias="refreshToken", default=None
    )


class SPasswordResetRequest(BaseModel):
    email: EmailStr


class SPasswordReset(BaseModel):
    token: str
    new_password: str = Field(alias="newPassword")


class SUserUpdate(BaseModel):
    bio: Optional[str] = Form(default=None)
    avatar: Optional[UploadFile] = Form(default=None)

    @classmethod
    async def as_form(
        cls,
        bio: Optional[str] = Form(default=None),
        avatar: Optional[UploadFile] = Form(default=None),
    ):
        return cls(bio=bio, avatar=avatar)


class SUserRead(BaseModel):
    id: int
    username: str
    avatar: str
    role: Optional[str] = Field(default=None)


class SUserProfile(SUserRead):
    bio: Optional[str] = Field(default=None)
    songs: list
    blocked: bool = Field(default=False)
    subscribed: bool = Field(default=False)
