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
    payments_enabled: bool = True
    payments_default_provider: str = "telegram_stars"
    payments_enable_telegram_stars: bool = True
    payments_enable_halyk: bool = False
    payments_enable_freedom: bool = False
    payments_enable_kaspi: bool = False
    payments_enable_crypto: bool = False
    payments_enable_aipay: bool = False
    premium_daily_forecast_limit: int = 50
    premium_daily_ai_limit: int = 100
    support_email: str = ""
    support_telegram_username: str = ""
    halyk_epay_enabled: bool = False
    halyk_epay_test_mode: bool = True
    halyk_epay_terminal_id: str = ""
    halyk_epay_client_id: str = ""
    halyk_epay_client_secret: str = ""
    halyk_epay_success_url: str = ""
    halyk_epay_failure_url: str = ""
    halyk_epay_webhook_secret: str = ""
    freedom_pay_enabled: bool = False
    freedom_pay_test_mode: bool = True
    freedom_pay_merchant_id: str = ""
    freedom_pay_secret_key: str = ""
    freedom_pay_result_url: str = ""
    freedom_pay_success_url: str = ""
    freedom_pay_failure_url: str = ""
    kaspi_enabled: bool = False
    kaspi_provider: str = ""
    kaspi_api_url: str = ""
    kaspi_api_key: str = ""
    kaspi_webhook_secret: str = ""
    crypto_enabled: bool = False
    crypto_provider: str = ""
    crypto_api_key: str = ""
    crypto_webhook_secret: str = ""
    crypto_allowed_assets: str = "USDT,TON"
    crypto_networks: str = "TON,TRC20"
    aipay_enabled: bool = False
    aipay_test_mode: bool = True
    aipay_api_url: str = ""
    aipay_secret: str = ""
    aipay_success_url: str = ""
    aipay_failure_url: str = ""
    aipay_callback_url: str = ""

    @property
    def telegram_initdata_token(self) -> str:
        return self.telegram_auth_bot_token or self.telegram_bot_token


settings = Settings()
