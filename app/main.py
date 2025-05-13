from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.users.router import router as user_router
from app.friends.router import router as friends_router
from app.chat.router import router as chat_router
from app.music import music_router

logger.add("logs/{time}.log", rotation="12:00")

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"message": "OK"}


app.include_router(user_router)
app.include_router(music_router)
app.include_router(friends_router)
app.include_router(chat_router)
