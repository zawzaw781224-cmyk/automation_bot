from telegram import Update
from telegram.ext import ContextTypes

from app.services.reply_service import generate_reply


async def business_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.business_message

    if not message or not message.text:
        return

    reply = generate_reply(message.text)

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=message.business_connection_id,
    )