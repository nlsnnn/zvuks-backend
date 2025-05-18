from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from app.users.router import router as user_router
from app.friends.router import router as friends_router
from app.chat.router import router as chat_router
from app.admin.router import router as admin_router
from app.music import music_router

from app.tq import broker
from app.error_handlers import register_error_handlers


logger.add("logs/app_{time}.log", rotation="12:00", level="INFO", encoding="utf-8")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        print(f"startup broker: {broker.is_worker_process=}")
        await broker.startup()
    yield
    if broker.is_worker_process:
        logger.info("Shutting down broker")
        await broker.shutdown()


app = FastAPI(lifespan=lifespan)
register_error_handlers(app)

origins = [
    "http://localhost:5173",
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
