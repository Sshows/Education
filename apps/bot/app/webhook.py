import os

from aiogram.types import Update
from fastapi import FastAPI, Header, HTTPException, Request
import uvicorn

from app.bot import bot, dp
from app.config import settings

app = FastAPI(title="ent-grant-bot")


@app.get('/health')
async def health():
    return {"status": "ok"}


@app.post('/webhook')
@app.post('/bot/webhook')
async def bot_webhook(request: Request, x_telegram_bot_api_secret_token: str | None = Header(default=None)):
    if settings.telegram_webhook_secret and x_telegram_bot_api_secret_token != settings.telegram_webhook_secret:
        raise HTTPException(401, 'Invalid webhook secret')
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {'ok': True}


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    uvicorn.run('app.webhook:app', host='0.0.0.0', port=port)
