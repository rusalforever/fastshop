from pydantic_settings import BaseSettings, SettingsConfigDict

class ProjectSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(env_file='.env')

settings = ProjectSettings(api_key="your_api_key_here")
print(settings.api_key)
