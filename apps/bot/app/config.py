from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    telegram_bot_token: str = ""
    telegram_webapp_url: str = "http://localhost:3000"
    telegram_webhook_secret: str = ""


settings = Settings()
