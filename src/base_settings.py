from typing import Optional

from pydantic import (
    BaseModel,
    conint,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class PostgresSettings(BaseModel):
    user: str = 'user'
    password: str = 'password'
    db: str = 'fastapi_shop'
    host: str = 'db'
    port: str = 5432
    url: str = 'postgresql+asyncpg://user:password@host.docker.internal:5432/fastapi_shop'


class AuthorizationSettings(BaseModel):
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: conint(gt=0) = 30
    crypt_schema: str = 'bcrypt'


class ProjectSettings(BaseSettings):
    api_key: str
    debug: Optional[bool] = True
    api_logger_format: Optional[str] = '%(levelname)s: %(asctime)s - %(message)s'

    postgres: PostgresSettings = PostgresSettings()
    auth: AuthorizationSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        frozen=True,
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


base_settings = ProjectSettings()
