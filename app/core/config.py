from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    postgres_scheme: str = 'postgresql+asyncpg'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'capacity_planning'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    database_echo: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=self.postgres_scheme,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
