from messaging import send_whatsapp_message

def send_message(platform: str, user_id: str, text: str):
    if platform == "whatsapp":
        send_whatsapp_message(phone=user_id, text=text)
