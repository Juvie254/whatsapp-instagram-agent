def build_context(user, missing):
    known = {
        "product": user.product,
        "color": user.color,
        "size": user.size,
        "quantity": user.quantity,
        "location": user.location,
    }

    known_clean = {k: v for k, v in known.items() if v}

    return {
        "known": known_clean,
        "missing": missing,
        "state": user.state,
        "rules": [
            "Ask only for missing information",
            "Do not repeat known details",
            "Be brief and conversational",
            "If state is READY_TO_CONFIRM, summarize and ask for confirmation",
            "If state is HUMAN_HANDOFF, stop selling and acknowledge handoff"
        ]
    }
