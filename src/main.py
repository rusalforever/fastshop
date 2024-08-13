from typing import Optional
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import FastAPI

class MongoSettings(BaseModel):
    url: str = Field(default='mongodb://mongo-db:27017/fastshop', env='MONGO_URL')
    direct_connection: bool = Field(default=False, env='MONGO_DIRECT_CONNECTION')
    const_status_prepared: str = Field(default='prepared', env='MONGO_CONST_STATUS_PREPARED')

class PostgresSettings(BaseModel):
    user: str = Field(default='user', env='POSTGRES_USER')
    password: SecretStr = Field(default='password', env='POSTGRES_PASSWORD')
    db: str = Field(default='fastapi_shop', env='POSTGRES_DB')
    host: str = Field(default='db', env='POSTGRES_HOST')
    port: int = Field(default=5432, env='POSTGRES_PORT')
    url: str = Field(default='postgresql+asyncpg://user:password@db:5432/fastapi_shop', env='POSTGRES_URL')

class AuthorizationSettings(BaseModel):
    secret_key: SecretStr = Field(default='default_secret_key', env='AUTH_SECRET_KEY')
    algorithm: str = Field(default='HS256', env='AUTH_ALGORITHM')
    access_token_expire_minutes: int = Field(default=30, gt=0, env='AUTH_ACCESS_TOKEN_EXPIRE_MINUTES')
    crypt_schema: str = Field(default='bcrypt', env='AUTH_CRYPT_SCHEMA')

class ProjectSettings(BaseSettings):
    api_key: SecretStr = Field(default="default_api_key", env='API_KEY')
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

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/config")
def read_config():
    return {
        "debug": base_settings.debug,
        "database_url": base_settings.postgres.url,
        "mongo_url": base_settings.mongo.url,
        "token_expiration": base_settings.auth.access_token_expire_minutes
    }
