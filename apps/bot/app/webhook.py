import logging
from contextlib import asynccontextmanager
from urllib.parse import urlsplit

from aiogram.types import MenuButtonWebApp, Update, WebAppInfo
from fastapi import FastAPI, Header, HTTPException, Request

from app.bot import BOT_COMMANDS, bot, dp
from app.config import settings

logger = logging.getLogger("ent-grant-bot")


def _safe_url(url: str | None) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}{parts.path}"


async def configure_telegram() -> None:
    if settings.telegram_auto_set_commands:
        try:
            await bot.set_my_commands(BOT_COMMANDS)
            logger.info("Telegram bot commands configured")
        except Exception:
            logger.exception("Failed to configure Telegram bot commands")

    if settings.telegram_auto_set_menu_button:
        try:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(
                    text="ENT Grant",
                    web_app=WebAppInfo(url=settings.telegram_webapp_url),
                )
            )
            logger.info("Telegram menu button configured for %s", _safe_url(settings.telegram_webapp_url))
        except Exception:
            logger.exception("Failed to configure Telegram menu button")

    if settings.telegram_auto_set_webhook:
        try:
            await bot.set_webhook(
                url=settings.telegram_webhook_url or "",
                secret_token=settings.telegram_webhook_secret,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"],
            )
            logger.info("Telegram webhook configured for %s", _safe_url(settings.telegram_webhook_url))
        except Exception:
            logger.exception("Failed to configure Telegram webhook")
            raise


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Bot service started on port %s", settings.port)
    await configure_telegram()
    try:
        yield
    finally:
        await bot.session.close()


app = FastAPI(title="ent-grant-bot", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bot"}


async def handle_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    expected_secret = settings.telegram_webhook_secret
    if expected_secret:
        if x_telegram_bot_api_secret_token != expected_secret:
            raise HTTPException(status_code=403, detail="Invalid webhook secret")
    elif settings.environment == "production":
        raise HTTPException(status_code=403, detail="Webhook secret is required")

    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    return await handle_webhook(request, x_telegram_bot_api_secret_token)


@app.post("/bot/webhook")
async def telegram_bot_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    return await handle_webhook(request, x_telegram_bot_api_secret_token)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.webhook:app", host="0.0.0.0", port=settings.port)
