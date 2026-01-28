def extract_entities(user, text: str):
    t = text.lower()

    # Product
    if "jacket" in t:
        user.product = "jacket"

    # Color
    for color in ["blue", "black", "red", "green", "grey"]:
        if color in t:
            user.color = color

    # Size
    if "large" in t or "l " in t:
        user.size = "L"
    elif "medium" in t or "m " in t:
        user.size = "M"
    elif "small" in t or "s " in t:
        user.size = "S"

    # Quantity
    if "one" in t or "1" in t:
        user.quantity = 1
    elif "two" in t or "2" in t:
        user.quantity = 2

    # Location
    if "nairobi" in t or "kasarani" in t or "mwiki" in t:
        user.location = text.strip()
