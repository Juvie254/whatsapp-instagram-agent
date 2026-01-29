from intent import classify_intent
from memory import get_or_create_user, save_message, cancel_followups
from entity_extractor import extract_entities
from state_manager import update_state
from missing_info import get_missing_info
from context_builder import build_context
from responder import generate_reply
from send import send_message
from handoff import handoff_to_human
from follow_up import schedule_follow_up

def process_message(phone: str, text: str):
    platform = "whatsapp"

    user, db = get_or_create_user(platform, phone)

    cancel_followups(user.id)
    save_message(user.id, "in", text)

    intent = classify_intent(text)

    extract_entities(user, text)
    update_state(user, intent)

    missing = get_missing_info(user)
    context = build_context(user, missing)

    reply = generate_reply(intent, text, context, user.state)

    send_message(platform, phone, reply)
    save_message(user.id, "out", reply, intent=intent)

    if user.state == "HUMAN_HANDOFF":
        db.commit()
        handoff_to_human(user)
        db.close()
        return

    if user.state not in ["DISENGAGED"]:
        schedule_follow_up(user.id, platform, phone)

    db.commit()
    db.close()


