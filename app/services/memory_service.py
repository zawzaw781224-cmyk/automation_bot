from app.database import SessionLocal
from app.models import Memory


def save_memory(
    telegram_user_id: int,
    memory_text: str,
):
    db = SessionLocal()

    try:
        memory = Memory(
            telegram_user_id=telegram_user_id,
            memory=memory_text,
        )

        db.add(memory)
        db.commit()

        print("MEMORY SAVED:", memory_text)

    except Exception as e:
        db.rollback()
        print("MEMORY SAVE ERROR:", e)

    finally:
        db.close()

def get_memories(
    telegram_user_id: int,
) -> list[str]:
    db = SessionLocal()

    try:
        memories = (
            db.query(Memory)
            .filter(
                Memory.telegram_user_id == telegram_user_id
            )
            .order_by(Memory.created_at.desc())
            .limit(20)
            .all()
        )

        return [
            memory.memory
            for memory in memories
        ]

    finally:
        db.close()