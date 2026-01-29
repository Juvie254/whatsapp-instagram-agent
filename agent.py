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

    # 1️⃣ Get or create user
    user, db = get_or_create_user(platform, phone)

    # 2️⃣ Save/update last seen
    user.last_seen = datetime.utcnow()
    db.commit()

    # 3️⃣ Detect intent
    intent = classify_intent(text)

    # 4️⃣ Extract entities from message
    extract_entities(user, text)

    # 5️⃣ Update user state based on intent and info
    update_state(user, intent)

    # 6️⃣ Determine missing information
    missing = get_missing_info(user)

    # 7️⃣ Build context for LLM
    context = build_context(user, missing)

    # 8️⃣ Generate reply
    reply = generate_reply(intent, text, context, user.state)

    # 9️⃣ Send reply to WhatsApp
    send_message(platform, phone, reply)

    #  🔟 Human handoff if ready
    if user.state == "HUMAN_HANDOFF":
        db.commit()
        handoff_to_human(user)
        db.close()
        return

    # 1️⃣1️⃣ Commit changes and close DB session
    db.commit()
    db.close()

