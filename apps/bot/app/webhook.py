from fastapi import FastAPI, Header, HTTPException, Request
from aiogram.types import Update

from app.bot import dp, bot
from app.config import settings

app = FastAPI(title="ent-grant-bot")


@app.post('/bot/webhook')
async def bot_webhook(request: Request, x_telegram_bot_api_secret_token: str | None = Header(default=None)):
    if settings.telegram_bot_token and x_telegram_bot_api_secret_token != settings.telegram_bot_token:
        raise HTTPException(401, 'Invalid webhook secret')
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {'ok': True}
