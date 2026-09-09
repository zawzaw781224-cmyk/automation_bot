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

    if sender:
        print("SENDER_ID:", sender.id)

    print("CHAT_ID:", message.chat.id)
    print("TEXT:", message.text)

    # Temporary: don't reply
    return