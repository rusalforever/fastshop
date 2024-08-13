from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class MongoSettings(BaseModel):
    url: str = Field(default='mongodb://mongo-db:27017/fastshop', env='MONGO_URL')
    direct_connection: bool = Field(default=False, env='MONGO_DIRECT_CONNECTION')
    const_status_prepared: str = 'prepared'

class PostgresSettings(BaseModel):
    user: str = Field(default='user', env='POSTGRES_USER')
    password: str = Field(default='password', env='POSTGRES_PASSWORD')
    db: str = Field(default='fastapi_shop', env='POSTGRES_DB')
    host: str = Field(default='db', env='POSTGRES_HOST')
    port: int = Field(default=5432, env='POSTGRES_PORT')
    url: str = Field(default='postgresql+asyncpg://user:password@db:5432/fastapi_shop', env='POSTGRES_URL')

class AuthorizationSettings(BaseModel):
    secret_key: str = Field(default='default_secret_key', env='AUTH_SECRET_KEY')
    algorithm: str = Field(default='HS256', env='AUTH_ALGORITHM')
    access_token_expire_minutes: int = Field(default=30, gt=0, env='ACCESS_TOKEN_EXPIRE_MINUTES')
    crypt_schema: str = Field(default='bcrypt', env='CRYPT_SCHEMA')

class ProjectSettings(BaseSettings):
    api_key: str = Field(default="default_api_key", env='API_KEY')
    debug: bool = Field(default=True, env='DEBUG')
    api_logger_format: str = Field(default='%(levelname)s: %(asctime)s - %(message)s', env='API_LOGGER_FORMAT')

    postgres: PostgresSettings = PostgresSettings()
    auth: AuthorizationSettings = AuthorizationSettings()
    mongo: MongoSettings = MongoSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        frozen=True,
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

base_settings = ProjectSettings()
