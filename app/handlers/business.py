from telegram import Update
from telegram.ext import ContextTypes

from app.services import reply_service
from app.services.ai_service import generate_ai_reply
from app.database import SessionLocal
from app.models import Message


MY_TELEGRAM_ID = 7230689165
VIP_TELEGRAM_ID = 7988070638


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

    print("SENDER ID:", sender.id)
    print("SENDER NAME:", sender.full_name)

    # ==========================================
    # 1. Save incoming user message
    # ==========================================

    db = SessionLocal()

    try:
        user_message = Message(
            telegram_user_id=sender.id,
            chat_id=message.chat.id,
            role="user",
            content=message.text,
        )

        db.add(user_message)
        db.commit()

        print("USER MESSAGE SAVED")

    except Exception as e:
        db.rollback()
        print("DATABASE ERROR:", e)

    finally:
        db.close()

    # ==========================================
    # 2. Owner's commands
    # ==========================================

    if sender.id == MY_TELEGRAM_ID:

        text = message.text.strip()

        if text.startswith("/setreply "):
            new_reply = text[len("/setreply "):].strip()

            if new_reply:
                reply_service.set_custom_reply(new_reply)

            return

        return

    # ==========================================
    # 3. Get conversation history
    # ==========================================

    db = SessionLocal()

    try:
        history_rows = (
            db.query(Message)
            .filter(
                Message.telegram_user_id == sender.id,
                Message.chat_id == message.chat.id,
            )
            .order_by(Message.created_at.desc())
            .limit(10)
            .all()
        )

        print("HISTORY ROWS:", len(history_rows))

        conversation_history = [
            {
                "role": row.role,
                "content": row.content,
            }
            for row in reversed(history_rows)
        ]

        print("CONVERSATION HISTORY:", conversation_history)

    finally:
        db.close()

    # ==========================================
    # 4. Generate AI reply
    # ==========================================

    reply = await generate_ai_reply(
        message.text,
        is_vip=(sender.id == VIP_TELEGRAM_ID),
        conversation_history=conversation_history,
    )

    # ==========================================
    # 5. Save AI reply
    # ==========================================

    db = SessionLocal()

    try:
        bot_message = Message(
            telegram_user_id=sender.id,
            chat_id=message.chat.id,
            role="assistant",
            content=reply,
        )

        db.add(bot_message)
        db.commit()

        print("AI REPLY SAVED")

    except Exception as e:
        db.rollback()
        print("DATABASE ERROR:", e)

    finally:
        db.close()

    # ==========================================
    # 6. Send reply to Telegram
    # ==========================================

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=message.business_connection_id,
    )