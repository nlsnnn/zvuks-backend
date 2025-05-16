from pydantic import BaseModel, Field


class SUserBlock(BaseModel):
    songs_archive: bool = Field(alias="songsArchive", default=True)
    albums_archive: bool = Field(alias="albumsArchive", default=True)


class SUserUnblock(BaseModel):
    songs_archive: bool = Field(alias="songsArchive", default=False)
    albums_archive: bool = Field(alias="albumsArchive", default=False)
