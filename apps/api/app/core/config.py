from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = "ent-grant-api"
    environment: str = "development"
    debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    web_url: str = "http://localhost:3000"

    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/ent_grant"
    redis_url: str = "redis://redis:6379/0"

    session_secret: str = "change_me"
    jwt_secret: str = "change_me"

    telegram_bot_token: str = ""
    telegram_webapp_url: str = "http://localhost:3000"
    telegram_webhook_url: str = ""
    telegram_webhook_secret: str = ""

    openai_api_key: str = ""


settings = Settings()
