from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.users.router import router as user_router
from app.friends.router import router as friends_router
from app.chat.router import router as chat_router
from app.admin.router import router as admin_router
from app.music import music_router

from app.logger import setup_logger
from app.tq import broker
from app.error_handlers import register_error_handlers


setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application")
    if not broker.is_worker_process:
        await broker.startup()
    yield
    logger.info("Shutting down FastAPI application")
    if broker.is_worker_process:
        await broker.shutdown()


app = FastAPI(lifespan=lifespan)
register_error_handlers(app)

origins = [
    "http://localhost:5173",
    "http://frontend",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"message": "OK"}


app.include_router(user_router)
app.include_router(music_router)
app.include_router(friends_router)
app.include_router(chat_router)
app.include_router(admin_router)
