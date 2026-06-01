from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi.extension import StrOrCallableStr
from sqlalchemy.engine import URL

MINIMAL_KEY_LENGTH = 32


class CommonSettings(BaseSettings):
    backend_host: str = 'http://localhost:5050'
    frontend_host: str = 'http://localhost:5555'


class AuthSettings(BaseSettings):
    private_key_path: str = 'private.pem'
    public_key_path: str = 'public.pem'
    algorithm: str = 'RS256'
    access_token_lifetime_seconds: int = int(timedelta(minutes=10).total_seconds())
    refresh_token_lifetime_seconds: int = int(timedelta(minutes=60).total_seconds())

    def get_private_key(self) -> str:
        key_path = Path(self.private_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f'Private key not found at {self.private_key_path}\n'
                f'Run: openssl genrsa -out {self.private_key_path} 2048'
            )

        key = key_path.read_text()

        if len(key) < MINIMAL_KEY_LENGTH:
            raise ValueError(
                f'Private key too short: {len(key)} characters (minimum 32 required)'
            )

        return key

    def get_public_key(self) -> str:
        key_path = Path(self.public_key_path)
        if not key_path.exists():
            raise FileNotFoundError(
                f'Public key not found at {self.public_key_path}\n'
                f'Run: openssl rsa -in private.pem -pubout -out {self.public_key_path}'
            )

        key = key_path.read_text()

        if len(key) < MINIMAL_KEY_LENGTH:
            raise ValueError(
                f'Private key too short: {len(key)} characters (minimum 32 required)'
            )

        return key


class DbSettings(BaseSettings):
    postgres_scheme: str = 'postgresql+asyncpg'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'capacity_planning'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    database_echo: bool = False

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=self.postgres_scheme,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)


class RoleSettings(BaseSettings):
    admin_email: str = 'admin@example.com'
    admin_password: str = 'Admin123!'
    admin_first_name: str = 'Admin'
    admin_last_name: str = 'Admin'
    admin_skills: str = 'System Admin'

    admin_role_code: str = 'admin'
    default_user_role_code: str = 'user'

    bootstrap_enabled: bool = True


class LimiterSettings(BaseSettings):
    default_limits: List[StrOrCallableStr] = ['10/minute']


class LoggingSettings(BaseSettings):
    file_name: str = 'my_log.log'


class EmailSettings(BaseSettings):
    username: EmailStr = "default@example.com"
    password: SecretStr = SecretStr("default")
    title: str = "Capacity Planning"
    port: int = 587
    server: str = 'smtp.gmail.com'
    from_name: str = 'Capacity Planning'
    notification_lifetime_seconds: int = 3600
    templates_dir: str = 'templates'
    base_url: str = 'http://locallost:8080/'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__',
    )

    db: DbSettings
    auth: AuthSettings
    role: RoleSettings
    limiter: LimiterSettings
    logging: LoggingSettings
    email: EmailSettings
    common: CommonSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
