from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(default='8352064418:AAG7BhxATbBNHxlyQ68LT4p7-Ocs7HOUUZU', json_schema_extra={'env': 'BOT_TOKEN'})
    api_base_url: str = Field(default='http://localhost:8000/tg-bot', json_schema_extra={'env': 'API_BASE_URL'})
    secret: str = Field(default='secret', json_schema_extra={'env': 'SECRET'})

    model_config = SettingsConfigDict(
        env_file="../.env",
        # env_file=".env",
        extra='ignore'
    )


settings = Settings()