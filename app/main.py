from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as user_router
from app.music.router import router as music_router
from app.friends.router import router as friends_router
from app.chat.router import router as chat_router


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

@app.get("/")
async def home_page():
    return {"message": "Hello"}


@app.get("/ping")
async def ping():
    return {"message": "OK"}


app.include_router(user_router)
app.include_router(music_router)
app.include_router(friends_router)
app.include_router(chat_router)