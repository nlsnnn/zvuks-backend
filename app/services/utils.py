import uuid
from fastapi import HTTPException, UploadFile

from app.config import get_s3_base_url, get_s3_client


class Utils:
    @staticmethod
    def get_file_format(file: UploadFile):
        return file.filename.split('.')[-1]

    @staticmethod
    async def upload_file(file: UploadFile, directory: str, allowed_formats: list[str]):
        file_format = Utils.get_file_format(file)
        if file_format not in allowed_formats:
            raise HTTPException(400, f"Недопустимый формат файла: {file_format}")

        file_content = await file.read()
        filename = f"{uuid.uuid4()}.{file_format}"
        path = f"{directory}/{filename}"

        s3_client = get_s3_client()
        await s3_client.upload_file(file_content, path)
        return f"{get_s3_base_url()}/{path}"
