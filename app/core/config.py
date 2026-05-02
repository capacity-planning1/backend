from datetime import timedelta
from functools import lru_cache
from urllib.parse import quote_plus
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

MINIMAL_KEY_LENGTH = 32

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
    access_token_lifetime_seconds: int = 600
    refresh_token_lifetime_seconds: int = 3600

    @property
    def access_token_lifetime_td(self) -> timedelta:
        return timedelta(seconds=self.access_token_lifetime_seconds)

    @property
    def refresh_token_lifetime_td(self) -> timedelta:
        return timedelta(seconds=self.refresh_token_lifetime_seconds)

    def get_private_key(self) -> str:
        key_path = Path(self.private_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f"Private key not found at {self.private_key_path}\n"
                f"Run: openssl genrsa -out {self.private_key_path} 2048"
            )

        key = key_path.read_text()

        if len(key) < MINIMAL_KEY_LENGTH:
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

        if len(key) < MINIMAL_KEY_LENGTH:
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

class RoleSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='ROLE_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    admin_email: str = "admin@example.com"
    admin_password: str = "Admin123!"
    admin_first_name: str = "Admin"
    admin_last_name: str = "Admin"
    admin_skills: str = "System Admin"

    admin_role_code: str = "admin"
    default_user_role_code: str = "user"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()
    role: RoleSettings = RoleSettings()

    bootstrap_enabled: bool = True

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db.postgres_user,
            password=self.db.postgres_password,
            host=self.db.postgres_host,
            port=self.db.postgres_port,
            database=self.db.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
