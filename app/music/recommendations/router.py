from fastapi import APIRouter, Response

from app.users.dependencies import (
    OptionalUserDep,
    CurrentUserDep,
)
from app.music.recommendations.service import RecommendationsService


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/popular/songs")
async def get_popular_songs(user: OptionalUserDep):
    return await RecommendationsService.popular_songs(user.id if user else None)


@router.get("/listen/{song_id}")
async def listen_song(song_id: int, user: CurrentUserDep):
    await RecommendationsService.add_listen(song_id, user.id)
    return Response()


@router.get("/new/songs")
async def get_new_songs(user: OptionalUserDep):
    return await RecommendationsService.get_new_songs(user.id if user else None)
