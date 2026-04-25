from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ent-grant-api"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ent_grant"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev"
    telegram_bot_token: str = ""
    telegram_webhook_secret: str = ""


settings = Settings()
