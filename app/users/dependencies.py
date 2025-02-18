from datetime import datetime, timezone
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import get_auth_data
from app.users.dao import UsersDAO
from app.users.models import User


class TokenDepends:
    """
    Класс-зависимость для проверки пользователя
    """

    def _get_token(self, request: Request):
        """
        Получение токена из куков
        """
        token = request.cookies.get('users_access_token')
        if not token: 
            self.__http_exception("Токен не найден")
        return token


    def _get_payload(self, token: str): 
        """
        Получение полезных данных с токена
        """
        try:
            auth_data = get_auth_data()
            payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        except JWTError:
            self.__http_exception("Токен не валидный")
        
        return payload
    

    def _check_time(self, payload: dict):
        """
        Проверка срока токена
        """
        expire = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.now(tz=timezone.utc)):
            self.__http_exception('Токен истек')


    async def get_current_user(self, request: Request) -> User | None:
        """
        Зависимость (получение пользователя)
        """
        token = self._get_token(request)
        payload = self._get_payload(token)
        self._check_time(payload)
        
        user_id = int(payload.get('sub'))
        if not user_id:
            self.__http_exception('Не найден ID пользователя')
        
        user = await UsersDAO.find_one_or_none_by_id(user_id)
        if not user:
            self.__http_exception('Пользователь не найден')
        
        return user
    

    async def get_current_admin_user(self, request: Request):
        current_user = await self.get_current_user(request)
        if current_user.is_admin:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав!' 
        )
    

    def __http_exception(self, detail: str):
        """
        Вызов ошибки 401
        """
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )