from typing import Literal
from urllib.parse import urljoin

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    telegram_bot_token: str = ""
    telegram_webapp_url: str = "http://localhost:3000"
    telegram_webhook_url: str | None = None
    telegram_webhook_secret: str = ""
    telegram_auto_set_webhook: bool = False
    telegram_auto_set_menu_button: bool = True
    telegram_auto_set_commands: bool = True
    api_url: str | None = None
    environment: Literal["development", "production"] = "development"
    port: int = 8080
    support_email: str = ""
    support_telegram_username: str = ""

    @model_validator(mode="after")
    def validate_runtime_config(self) -> "Settings":
        if self.environment == "production" and not self.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required in production")
        if self.environment == "production" and not self.telegram_webhook_secret:
            raise ValueError("TELEGRAM_WEBHOOK_SECRET is required in production")
        if self.telegram_auto_set_webhook and not self.telegram_webhook_url:
            raise ValueError("TELEGRAM_WEBHOOK_URL is required when TELEGRAM_AUTO_SET_WEBHOOK=true")
        return self

    def webapp_url(self, path: str = "") -> str:
        base = self.telegram_webapp_url.rstrip("/") + "/"
        return urljoin(base, path.lstrip("/"))


settings = Settings()
