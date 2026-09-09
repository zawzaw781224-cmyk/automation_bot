import asyncio

from app.services.ai_service import generate_ai_reply


async def main():
    reply = await generate_ai_reply(
        "ငါ့အကြောင်း နည်းနည်းပြောပြပါ"
    )

    print("AI Reply:")
    print(reply)


asyncio.run(main())