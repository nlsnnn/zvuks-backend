from fastapi import APIRouter, Depends

from app.music.album import AlbumDAO, AlbumCreate
from app.music.album.service import AlbumService
from app.users.dependencies import CurrentUserDep, OptionalUserDep


router = APIRouter(prefix="/album", tags=["Album"])


@router.get("/")
async def get_all_albums(user: OptionalUserDep):
    albums = await AlbumService.get_all_albums(user_id=user.id if user else None)
    return {"albums": albums}


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
    album, songs = await AlbumService.add_album(album_data, user_data)

    return {
        "album": {
            "id": album.id,
            "name": album_data.name,
            "release_date": album_data.release_date,
            "songs": songs,
        }
    }


@router.patch("/{album_id}")
async def update_album(album_id: int):
    album = await AlbumDAO.find_one_or_none_by_id(album_id)
    return {"message": "ok"}


@router.delete("/{album_id}")
async def delete_album(album_id: int):
    await AlbumDAO.delete(id=album_id)
    return {"message": f"Album {album_id} successfull deleted!"}
