TERMINAL_STATES = [
    "NOT_INTERESTED",
    "HUMAN_HANDOFF",
    "FOLLOW_UP_SENT"
]

def should_respond(user_state: str, intent: str) -> bool:
    # If user clearly disengaged, do NOT re-sell
    if user_state == "NOT_INTERESTED" and intent in ["OTHER", "ASK_PRICE"]:
        return False

    return True


def next_state(current_state: str, intent: str) -> str:
    if intent == "OBJECTION":
        return "NOT_INTERESTED"

    if intent == "BUY":
        return "READY_TO_BUY"

    if intent == "ASK_PRICE":
        return "ASKING_PRICE"

    if intent == "INTEREST":
        return "INTERESTED"

    return current_state
