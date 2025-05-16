from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError

from app.admin.exceptions import admin_exception_handler


def register_error_handlers(app: FastAPI):
    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(request: Request, exc: ValidationError):
        logger.error(exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Unhandled error"},
        )

    @app.exception_handler(DatabaseError)
    def handle_db_error(request: Request, exc: DatabaseError):
        logger.error(f"Database error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Service temporarily dont work"},
        )

    @app.exception_handler(Exception)
    def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )

    for exc_class, handler in admin_exception_handler:
        app.add_exception_handler(exc_class, handler)
