def update_state(user, intent: str):
    """
    Determines the NEXT user state based on intent and collected info.
    Exactly ONE state transition per call.
    """

    # 🔒 Terminal state
    if user.state == "HUMAN_HANDOFF":
        return

    # 🛑 Hard intent override
    if intent == "BUY":
        user.state = "HUMAN_HANDOFF"
        return

    # 😕 Soft objection (pause selling)
    if intent == "OBJECTION":
        user.state = "OBJECTION"
        return

    # 🆕 New user enters discovery
    if user.state == "NEW":
        user.state = "DISCOVERY"
        return

    # 🔍 Check if enough info collected
    has_core_details = all([
        user.product,
        user.size,
        user.quantity,
        user.location
    ])

    if has_core_details and user.state != "READY_TO_CONFIRM":
        user.state = "READY_TO_CONFIRM"
        return

    # 📦 Partial info collected
    if user.product and user.state == "DISCOVERY":
        user.state = "DETAILS_COLLECTED"
        return

