from telegram import Update
from telegram.ext import ContextTypes


async def business_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.business_message

    if not message:
        return

    sender = message.from_user

    if not sender:
        return

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Your Telegram ID is: {sender.id}",
        business_connection_id=message.business_connection_id,
    )