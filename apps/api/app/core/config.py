from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ent-grant-api"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ent_grant"
    redis_url: str = "redis://localhost:6379/0"
    session_secret: str = "dev"
    secret_key: str = "dev"
    telegram_bot_token: str = ""
    telegram_auth_bot_token: str = ""
    telegram_webhook_secret: str = ""
    environment: Literal["development", "production"] = "development"
    debug: bool = True

    @property
    def telegram_initdata_token(self) -> str:
        return self.telegram_auth_bot_token or self.telegram_bot_token


settings = Settings()
