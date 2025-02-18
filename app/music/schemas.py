from datetime import datetime
# from fastapi import UploadFile, Form, File
from pydantic import BaseModel, Field


# class SongAdd(BaseModel):
#     name: str = Form(description='Название песни')
#     release_date: datetime = Form(description='Дата релиза песни')
#     song: UploadFile = File(description="Файл песни")


class AlbumAdd(BaseModel):
    name: str = Field(description='Название песни')
    release_date: datetime = Field(description='Дата релиза песни')


class SongUpdate(BaseModel):
    name: str = Field(description='Название песни')  
    release_date: datetime = Field(description='Дата релиза песни')