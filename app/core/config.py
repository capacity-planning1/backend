from functools import lru_cache
from urllib.parse import quote_plus
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    MINIMAL_KEY_LENGTH = 32

    model_config = SettingsConfigDict(
        env_prefix='AUTH_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    private_key_path: str = 'private.pem'
    public_key_path: str = 'public.pem'
    algorithm: str = 'RS256'
    access_token_lifetime_seconds: int = 600
    refresh_token_lifetime_seconds: int = 3600

    def get_private_key(self) -> str:
        key_path = Path(self.private_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f"Private key not found at {self.private_key_path}\n"
                f"Run: openssl genrsa -out {self.private_key_path} 2048"
            )

        key = key_path.read_text()

        if len(key) < self.MINIMAL_KEY_LENGTH:
            raise ValueError(
                f"Private key too short: {len(key)} characters (minimum 32 required)"
            )

        return key

    def get_public_key(self) -> str:
        key_path = Path(self.public_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f"Public key not found at {self.public_key_path}\n"
                f"Run: openssl rsa -in private.pem -pubout -out {self.public_key_path}"
            )

        key = key_path.read_text()

        if len(key) < self.MINIMAL_KEY_LENGTH:
            raise ValueError(
                f"Private key too short: {len(key)} characters (minimum 32 required)"
            )

        return key


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
