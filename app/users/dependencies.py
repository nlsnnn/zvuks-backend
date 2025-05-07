from datetime import datetime, timezone
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError

from app.config import get_auth_data
from app.users.dao import UsersDAO
from app.users.models import User
from app.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    NoJwtException,
    NoUserIdException,
    ForbiddenException,
    NoUserException,
)


def get_token(request: Request):
    """
    Получение токена из куков
    """
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFoundException
    return token


def get_payload(token: str):
    """
    Получение полезных данных с токена
    """
    try:
        auth_data = get_auth_data()
        if auth_data["algorithm"] not in {"HS256", "HS384", "HS512"}:
            raise ValueError("Недопустимый алгоритм JWT")
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise NoJwtException

    return payload


def check_time(payload: dict):
    """
    Проверка срока токена
    """
    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(tz=timezone.utc)):
        raise TokenExpiredException


async def get_current_user(request: Request) -> Optional[User]:
    """
    Зависимость (получение пользователя)
    """
    token = get_token(request)
    payload = get_payload(token)
    check_time(payload)

    user_id = int(payload.get("sub"))
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise NoUserException

    return user


async def get_optional_user(request: Request) -> Optional[User]:
    """
    Зависимость (опциональное получения пользователя)
    """
    try:
        return await get_current_user(request)
    except HTTPException as e:
        if e.status_code in (401, 403):
            return None
        raise


async def get_current_admin_user(request: Request):
    current_user = await get_current_user(request)
    if current_user.is_admin:
        return current_user
    raise ForbiddenException


CurrentUserDep = Annotated[User, Depends(get_current_user)]
OptionalUserDep = Annotated[Optional[User], Depends(get_optional_user)]
CurrentAdminDep = Annotated[User, Depends(get_current_admin_user)]
