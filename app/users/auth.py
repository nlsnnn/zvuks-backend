from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import EmailStr

from app.config import get_auth_data
from app.exceptions import NoJwtException
from app.users.dao import UsersDAO
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def create_reset_password_token(email: str) -> str:
    data = {"sub": email, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
    auth_data = get_auth_data()
    token = jwt.encode(data, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return token


def verify_reset_password_token(token: str) -> str:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        email = payload.get("sub")
        if not email:
            raise NoJwtException
        return email
    except JWTError:
        raise NoJwtException


async def authenticate_user(identifier: EmailStr | str, password: str) -> User | str:
    user = await UsersDAO.find_one_or_none(email=identifier)
    if not user:
        user = await UsersDAO.find_one_or_none(username=identifier)
        if not user:
            return "Пользователя не существует"
    if verify_password(plain_password=password, hashed_password=user.password) is False:
        return "Неверный пароль"
    return user 