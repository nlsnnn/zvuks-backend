from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.users.dependencies import get_current_user
from app.users.models import User
from app.music.recommendations.service import RecommendationsService


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/popular/songs")
async def get_popular_songs(user: Annotated[User, Depends(get_current_user, use_cache=True)]):
    return await RecommendationsService.popular_songs(user.id)


@router.get("/listen/{song_id}")
async def listen_song(song_id: int, user: Annotated[User, Depends(get_current_user)]):
    await RecommendationsService.add_listen(song_id, user.id)
    return Response()


@router.get("/new/songs")
async def get_new_songs(user: Annotated[User, Depends(get_current_user)]):
    return await RecommendationsService.get_new_songs(user.id)
