import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

from app.handlers.business import business_message_handler
from app.config.settings import TELEGRAM_BOT_TOKEN


telegram_app = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)


# Business Messages
telegram_app.add_handler(
    MessageHandler(
        filters.UpdateType.BUSINESS_MESSAGE,
        business_message_handler,
    )
)


app = FastAPI()


@app.post("/api/telegram")
async def telegram_webhook(request: Request):

    data = await request.json()

    update = Update.de_json(
        data=data,
        bot=telegram_app.bot,
    )

    await telegram_app.initialize()

    try:
        await telegram_app.process_update(update)
    finally:
        await telegram_app.shutdown()

    return PlainTextResponse("OK")