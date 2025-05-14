from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.music.album import AlbumDAO, AlbumCreate
from app.music.album.service import AlbumService
from app.music.exceptions import AlbumCreateException
from app.users.dependencies import CurrentUserDep, OptionalUserDep


router = APIRouter(prefix="/album", tags=["Album"])


@router.get("/")
async def get_all_albums(user: OptionalUserDep):
    albums = await AlbumService.get_all_albums(user_id=user.id if user else None)
    return {"albums": albums}


@router.get("/search")
async def search_albums(query: str, user: OptionalUserDep):
    return await AlbumService.search_albums(query, user.id if user else None)


@router.get("/{album_id}")
async def get_album(album_id: int, user: OptionalUserDep):
    album = await AlbumService.get_album(album_id, user.id if user else None)
    return {"album": album}


@router.get("/{album_id}/songs")
async def get_album_songs(album_id: int, user: OptionalUserDep):
    songs = await AlbumService.get_album_songs(album_id, user.id if user else None)
    return {"songs": songs}


@router.post("/")
async def add_album(
    user_data: CurrentUserDep,
    album_data: AlbumCreate = Depends(AlbumCreate.as_form),
) -> dict:
    try:
        await AlbumService.add_album(album_data, user_data)
        return {"message": "Альбом успешно создан"}
    except AlbumCreateException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@router.patch("/{album_id}")
async def update_album(album_id: int):
    album = await AlbumDAO.find_one_or_none_by_id(album_id)
    return {"message": "ok"}


@router.delete("/{album_id}")
async def delete_album(album_id: int):
    await AlbumDAO.delete(id=album_id)
    return {"message": f"Album {album_id} successfull deleted!"}
