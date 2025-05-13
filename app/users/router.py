from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.config import get_default_avatar
from app.email.service import EmailService
from app.exceptions import NoUserException
from app.users.auth import (
    authenticate_user,
    create_access_token,
    create_reset_password_token,
    get_password_hash,
    verify_reset_password_token,
)
from app.users.dao import UsersDAO
from app.users.dependencies import CurrentUserDep, CurrentAdminDep
from app.users.schemas import (
    SPasswordReset,
    SUserAuth,
    SPasswordResetRequest,
    SUserRegister,
    SUserProfile,
    SUserRead,
    SUserUpdate,
)
from app.users.service import UserService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )

    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    avatar_path = get_default_avatar()
    await UsersDAO.add(avatar_path=avatar_path, **user_dict)
    return {"message": "success"}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    user = await authenticate_user(user_data.identifier, user_data.password)
    if type(user) is str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=user)

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.post("/password-reset")
async def request_password_reset(data: SPasswordResetRequest):
    user = await UsersDAO.find_one_or_none(email=data.email)
    if not user:
        raise NoUserException

    token = create_reset_password_token(data.email)
    reset_link = f"http://localhost:5173/reset-password/confirm/{token}"
    await EmailService.send_reset_password(user, reset_link)
    return {"message": "Письмо для сброса пароля отправлено"}


@router.post("/password-reset/confirm")
async def reset_password(data: SPasswordReset):
    email = verify_reset_password_token(data.token)
    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise NoUserException

    hashed_password = get_password_hash(data.new_password)
    await UsersDAO.update(filter_by={"email": email}, password=hashed_password)
    return {"message": "Пароль успешно изменен"}


@router.post("/user/update", response_model=SUserRead)
async def update_user(
    user_data: CurrentUserDep,
    data: SUserUpdate = Depends(SUserUpdate.as_form),
):
    data = await UserService.update_user(data, user_data)
    return data


@router.get("/me/", response_model=SUserRead)
async def get_me(user_data: CurrentUserDep):
    return UserService.get_user_dto(user_data)


@router.get("/all_users/")
async def get_all_users(
    user_data: CurrentAdminDep,
):
    users = await UsersDAO.find_all()
    return {"users": users}


@router.get("/user/{user_id}", response_model=SUserRead)
async def get_user(user_id: int, user_data: CurrentAdminDep):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    data = UserService.get_user_dto(user)
    return data


@router.get("/user/search/")
async def find_user(query: str, user_data: CurrentUserDep):
    users = await UsersDAO.search_users_with_status(query, user_data.id)
    return {"users": users}


@router.get("/user/profile/{user_id}", response_model=SUserProfile)
async def get_user_profile(user_id: int, user_data: CurrentUserDep):
    profile_data = await UserService.get_profile(user_id)

    return profile_data


@router.post("/user/subscribe/{user_id}")
async def subscribe_user(user_id: int, user_data: CurrentUserDep):
    try:
        await UserService.subscribe_user(user_id, user_data.id)
        return {"message": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/unsubscribe/{user_id}")
async def unsubscribe_user(user_id: int, user_data: CurrentUserDep):
    try:
        await UserService.unsubscribe_user(user_id, user_data.id)
        return {"message": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
