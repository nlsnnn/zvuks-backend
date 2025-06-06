from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import status, HTTPException


class ZvuksException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code



class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")


UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')


IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail="Неверная почта или пароль")


NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Токен невалидный!")


NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail="Не найден ID пользователя")


ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                   detail="Недостаточно прав!")

AlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                       detail='Объект уже существует')

NoUserException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователь не найден")

NotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Не найдено")