from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str = ""
    telegram_mini_app_url: str = "http://localhost:3000"


settings = Settings()
