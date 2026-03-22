from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_host: str = Field('localhost', alias='POSTGRES_HOST')
    postgres_port: int = Field(5432, alias='POSTGRES_PORT')
    postgres_db: str = Field('capacity_planning', alias='POSTGRES_DB')
    postgres_user: str = Field('postgres', alias='POSTGRES_USER')
    postgres_password: str = Field('postgres', alias='POSTGRES_PASSWORD')
    database_echo: bool = Field(False, alias='DB_ECHO')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def database_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f"{quote_plus(self.postgres_user)}:{quote_plus(self.postgres_password)}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
