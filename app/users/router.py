from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import TokenDepends
from app.users.models import User
from app.users.schemas import SUserAuth, SUserRegister


router = APIRouter(prefix="/auth", tags=['Auth'])

token_depends = TokenDepends()

@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Пользователь уже существует')
    
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": 'success'}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    print(f'{response=}')
    user = await authenticate_user(user_data.email, user_data.password)
    if type(user) is str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": 'Пользователь успешно вышел из системы'}


@router.get("/me/")
async def get_me(user_data: User = Depends(token_depends.get_current_user)):
    return user_data


@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(token_depends.get_current_admin_user)):
    users = await UsersDAO.find_all()
    return {"users": users}


@router.get("/user/{user_id}")
async def get_user(user_id: int, user_data: User = Depends(token_depends.get_current_admin_user)): 
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    return {"user": user}


@router.get("/user/search/")
async def find_user(query: str, user_data: User = Depends(token_depends.get_current_user)):
    users = await UsersDAO.search_users(query)
    return {"users": [{'id': user.id, 'username': user.username} for user in users]}