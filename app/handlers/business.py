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

    # Debug: show sender information
    print("========== BUSINESS MESSAGE ==========")
    print("Chat ID:", message.chat.id)

    if message.from_user:
        print("Sender ID:", message.from_user.id)
        print("Sender Username:", message.from_user.username)
        print("Sender Name:", message.from_user.full_name)

    print("Message:", message.text)
    print("======================================")

    reply = generate_reply(message.text)

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=message.business_connection_id,
    )