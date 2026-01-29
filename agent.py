from datetime import datetime
from intent import classify_intent
from memory import get_or_create_user
from entity_extractor import extract_entities
from state_manager import update_state
from missing_info import get_missing_info
from context_builder import build_context
from responder import generate_reply
from send import send_message
from handoff import handoff_to_human

def process_message(phone: str, text: str):
    platform = "whatsapp"

    # 1️⃣ Get user + DB session
    user, db = get_or_create_user(platform, phone)

    try:
        # 2️⃣ Detect intent
        intent = classify_intent(text)

        # 3️⃣ Extract entities
        extract_entities(user, text)

        # 4️⃣ Update state
        update_state(user, intent)

        # 5️⃣ Check missing info
        missing = get_missing_info(user)

        # 6️⃣ Build LLM context
        context = build_context(user, missing)

        # 7️⃣ Generate reply
        reply = generate_reply(intent, text, context, user.state)

        # 8️⃣ Send message
        send_message(platform, phone, reply)

        # 9️⃣ Optional human handoff
        if user.state == "HUMAN_HANDOFF":
            handoff_to_human(user)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

