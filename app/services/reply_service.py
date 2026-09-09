AUTO_REPLY_ENABLED = True


def generate_reply(message_text: str) -> str:
    text = message_text.lower().strip()

    if text in ["hi", "hello", "ဟယ်လို", "မင်္ဂလာပါ"]:
        return "ဟယ်လို 👋 အခုတော့ မအားသေးလို့ နောက်မှ ပြန်ပြောပေးမယ်နော် 😊"

    if "နေကောင်း" in text:
        return "နေကောင်းပါတယ် 😊 မေးပေးလို့ ကျေးဇူးပါ။"

    return "Message ရရှိပါတယ် 😊 အခုတော့ ခဏမအားသေးလို့ နောက်မှ ပြန်ပြောပေးမယ်နော်။"