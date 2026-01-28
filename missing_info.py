def get_missing_info(user):
    missing = []

    if not user.product:
        missing.append("product")
    if not user.size:
        missing.append("size")
    if not user.quantity:
        missing.append("quantity")
    if not user.location:
        missing.append("delivery location")

    return missing
