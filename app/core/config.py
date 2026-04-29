from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='AUTH_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    private_key_path: str = 'private.pem'
    public_key_path: str = 'public.pem'
    algorithm: str = 'RS256'
    access_token_lifetime_seconds: int = 900
    refresh_token_lifetime_seconds: int = 604800

    def get_private_key(self) -> str:
        key_path = Path(self.private_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f'Private key not found at {self.private_key_path}\n'
                f'Run: openssl genrsa -out {self.private_key_path} 2048'
            )
        return key_path.read_text()

    def get_public_key(self) -> str:
        key_path = Path(self.public_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f'Public key not found at {self.public_key_path}\n'
                f'Run: openssl rsa -in private.pem -pubout -out {self.public_key_path}'
            )
        return key_path.read_text()


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    postgres_scheme: str = 'postgresql+asyncpg'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'capacity_planning'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    database_echo: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()

    @property
    def database_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f'{quote_plus(self.db.postgres_user)}:{quote_plus(self.db.postgres_password)}'
            f'@{self.db.postgres_host}:{self.db.postgres_port}/{self.db.postgres_db}'
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
