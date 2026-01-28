def update_state(user, intent: str):
    if user.state == "HUMAN_HANDOFF":
        return

    if intent in ["OBJECTION"]:
        user.state = "DISENGAGED"
        return

    if user.state == "NEW":
        user.state = "DISCOVERY"

    if user.product and user.state == "DISCOVERY":
        user.state = "DETAILS_COLLECTED"

    if (
        user.product
        and user.size
        and user.quantity
        and user.location
        and user.state == "DETAILS_COLLECTED"
    ):
        user.state = "READY_TO_CONFIRM"

    if intent == "BUY" and user.state == "READY_TO_CONFIRM":
        user.state = "HUMAN_HANDOFF"
