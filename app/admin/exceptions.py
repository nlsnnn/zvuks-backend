from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import ZvuksException


class AdminException(ZvuksException):
    pass


def handle_admin_error(request: Request, exc: AdminException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


admin_exception_handler = [(AdminException, handle_admin_error)]
