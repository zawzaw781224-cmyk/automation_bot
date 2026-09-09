from telegram import Update
from telegram.ext import ContextTypes

from app.services import reply_service
from app.services.ai_service import generate_ai_reply


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

    # Owner's commands
    if sender.id == MY_TELEGRAM_ID:

        text = message.text.strip()

        if text.startswith("/setreply "):
            new_reply = text[len("/setreply "):].strip()

            if new_reply:
                reply_service.set_custom_reply(new_reply)

            return

        return

    # Auto reply OFF
    if not reply_service.AUTO_REPLY_ENABLED:
        return

    # Generate reply with AI
    reply = await generate_ai_reply(message.text)

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=message.business_connection_id,
    )