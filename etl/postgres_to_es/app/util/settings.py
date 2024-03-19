from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    es_host: str = Field(env='ES_HOST')
    es_port: str = Field(env='ES_PORT')
    es_index: str = Field(env='ES_INDEX')
    db_host: str = Field(env='DB_HOST')
    db_port: str = Field(env='DB_PORT')
    db_name: str = Field(env='DB_NAME')
    db_user: str = Field(env='DB_USER')
    db_password: str = Field(env='DB_PASSWORD')
    db_schema: str = Field(env='DB_SCHEMA')
    default_updated_at: str = Field(env='DEFAULT_UPDATED_AT')


_settings = Settings(_env_file='../.env')


def retrieve_settings():
    return _settings
