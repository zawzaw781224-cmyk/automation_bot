CUSTOM_REPLY = (
    "Message ရရှိပါတယ် 😊 "
    "အခုတော့ ခဏမအားသေးလို့ နောက်မှ ပြန်ပြောပေးမယ်နော်။"
)


def set_custom_reply(reply: str):
    global CUSTOM_REPLY
    CUSTOM_REPLY = reply


def generate_reply(message_text: str) -> str:
    return CUSTOM_REPLY