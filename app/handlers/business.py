from telegram import Update
from telegram.ext import ContextTypes

from app.services.reply_service import (
    generate_reply,
    set_auto_reply,
    AUTO_REPLY_ENABLED,
)


MY_TELEGRAM_ID = 7230689165


async def business_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.business_message

    if not message or not message.text:
        return

    sender = message.from_user

    if not sender:
        return

    # Don't reply to my own messages
    if sender.id == MY_TELEGRAM_ID:

        # Control commands
        if message.text.lower().strip() == "/on":
            set_auto_reply(True)
            return

        if message.text.lower().strip() == "/off":
            set_auto_reply(False)
            return

        return

    # Don't reply when auto-reply is disabled
    if not AUTO_REPLY_ENABLED:
        return

    reply = generate_reply(message.text)

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=message.business_connection_id,
    )