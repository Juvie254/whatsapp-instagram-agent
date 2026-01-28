from intent import classify_intent
from responder import generate_reply
from memory import save_message, cancel_followups
from follow_up import schedule_follow_up
from handoff import handoff_to_human
from db import SessionLocal
from models import User
from send import send_message


def process_message(phone: str, text: str):
    print(f"🧠 Agent received message | {phone}: {text}")

    platform = "whatsapp"
    platform_user_id = phone
    db = SessionLocal()

    # ---------- USER ----------
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

    cancel_followups(user.id)
    save_message(user.id, "in", text)

    # ---------- INTENT ----------
    intent = classify_intent(text)
    print("🎯 Detected intent:", intent)

    # ---------- HUMAN HANDOFF ----------
    if user.state == "HUMAN_HANDOFF":
        db.close()
        return

    # ---------- STATE UPDATE (NO SENDING HERE) ----------
    if intent == "ASK_PRICE":
        user.state = "PRICE"

    elif intent == "BUY":
        user.state = "HUMAN_HANDOFF"
        db.commit()
        handoff_to_human(user)
        db.close()
        return

    elif intent == "OBJECTION":
        user.state = "OBJECTION"

    elif intent == "INTEREST":
        user.state = "INTEREST"

    else:
        user.state = "ACTIVE"

    db.commit()

    # ---------- LLM REPLY (SINGLE SOURCE OF TRUTH) ----------
    reply = generate_reply(intent, text)

    if not reply:
        reply = "Hi 👋 How can I help you today?"

    print("📤 FINAL REPLY TO USER:", reply)
    send_message(platform, platform_user_id, reply)

    # ---------- FOLLOW-UP ----------
    if user.state != "HUMAN_HANDOFF":
        schedule_follow_up(
            user_id=user.id,
            platform=platform,
            platform_user_id=platform_user_id
        )

    db.close()
