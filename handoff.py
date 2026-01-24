from memory import cancel_followups
from messaging import send_whatsapp_message

BUSINESS_OWNER_PHONE = "2547XXXXXXXX"


def handoff_to_human(user):
    # 1. Stop all automation
    cancel_followups(user.id)

    # 2. Notify customer
    send_whatsapp_message(
        user.platform_user_id,
        "Thanks! A human will take over shortly to complete your order 😊"
    )

    # 3. Notify business owner
    send_whatsapp_message(
        BUSINESS_OWNER_PHONE,
        f"🔥 New hot lead\nPhone: {user.platform_user_id
}\nStatus: Ready to buy"
    )
