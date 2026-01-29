def get_missing_info(user):
    # States where we should NOT ask for details
    if user.state in ["HUMAN_HANDOFF", "DISENGAGED"]:
        return []

    missing = []

    if user.state in ["NEW", "DISCOVERY", "DETAILS_COLLECTED"]:
        if not user.product:
            missing.append("product")

        if user.product:
            if not user.size:
                missing.append("size")

            if not user.quantity:
                missing.append("quantity")

            if not user.location:
                missing.append("delivery location")

    return missing
