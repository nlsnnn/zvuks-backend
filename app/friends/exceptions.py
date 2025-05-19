from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import ZvuksException


class FriendsException(ZvuksException):
    pass


def handle_friends_error(request: Request, exc: FriendsException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


friends_exception_handler = [(FriendsException, handle_friends_error)]
