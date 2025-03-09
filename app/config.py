import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.services.s3 import S3Client


BASE_DIR = Path(__file__).parent.parent


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str


class S3Config(BaseModel):
    access_key: str
    secret_key: str
    bucket_name: str
    endpoint: str = "https://storage.yandexcloud.net"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APPLICATION__",
    )

    db: DatabaseConfig
    jwt: JWTConfig
    s3: S3Config


settings = Settings()


def get_db_url():
    url = (f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}@"
            f"{settings.db.host}:{settings.db.port}/{settings.db.name}")
    return url


def get_auth_data():
    return {"secret_key": settings.jwt.secret_key, "algorithm": settings.jwt.algorithm}


def get_s3_client() -> S3Client:
    return S3Client(
        access_key=settings.s3.access_key,
        secret_key=settings.s3.secret_key,
        bucket_name=settings.s3.bucket_name,
        endpoint_url=settings.s3.endpoint,
    )


def get_song_path():
    pass
