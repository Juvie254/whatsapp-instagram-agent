from intent import classify_intent
from memory import save_message, cancel_followups
from follow_up import schedule_follow_up
from handoff import handoff_to_human
from db import SessionLocal
from models import User
from send import send_message


def process_message(phone: str, text: str):
    platform = "whatsapp"
    platform_user_id = phone

    db = SessionLocal()

    # Get or create user
    user = (
        db.query(User)
        .filter(
            User.platform == platform,
            User.platform_user_id == platform_user_id
        )
        .first()
    )

    if not user:
        user = User(
            platform=platform,
            platform_user_id=platform_user_id,
            state="NEW"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # User replied → cancel follow-ups
    cancel_followups(user.id)

    # Save inbound message
    save_message(user.id, "in", text)

    intent = classify_intent(text)

    # 🚫 Human already handling
    if user.state == "HUMAN_HANDOFF":
        db.close()
        return

    # ---------- SALES LOGIC ----------

    if intent == "ASK_PRICE":
        send_message(platform, platform_user_id,
                     "This jacket is KES 2,500. Free delivery within Nairobi 😊")
        user.state = "ASKING_PRICE"

    elif intent == "INTEREST":
        send_message(platform, platform_user_id,
                     "Great choice! Would you like to place an order?")
        user.state = "INTERESTED"

    elif intent == "OBJECTION":
        send_message(platform, platform_user_id,
                     "Totally understand 😊 Would a small discount help?")
        user.state = "OBJECTION"

    elif intent == "BUY":
        send_message(platform, platform_user_id,
                     "Awesome! I’m connecting you with a human to complete your order 👌")
        user.state = "HUMAN_HANDOFF"
        db.commit()
        handoff_to_human(user)
        db.close()
        return

    else:
        send_message(platform, platform_user_id,
                     "Hi 👋 Let me know if you'd like the price or want to order.")

    db.commit()

    # ---------- FOLLOW-UP ----------
    if user.state != "HUMAN_HANDOFF":
        schedule_follow_up(
            user_id=user.id,
            platform=platform,
            platform_user_id=platform_user_id
        )

    db.close()
print(f"🤖 Agent processing message from {phone}: {text}")
