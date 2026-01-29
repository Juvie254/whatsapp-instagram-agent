import re

def extract_entities(user, text: str):
    """
    Extracts structured entities from user text.
    Updates user object only when confident.
    Returns a dict of extracted fields.
    """

    extracted = {}
    t = text.lower()

    # ----------------
    # Product
    # ----------------
    if not user.product and "jacket" in t:
        user.product = "jacket"
        extracted["product"] = "jacket"

    # ----------------
    # Color
    # ----------------
    colors = ["blue", "black", "red", "green", "grey"]
    for color in colors:
        if re.search(rf"\b{color}\b", t):
            user.color = color
            extracted["color"] = color
            break

    # ----------------
    # Size
    # ----------------
    size_map = {
        "large": "L",
        "medium": "M",
        "small": "S",
        " xl": "XL",
        " l ": "L",
        " m ": "M",
        " s ": "S"
    }

    for key, val in size_map.items():
        if key in t:
            user.size = val
            extracted["size"] = val
            break

    # ----------------
    # Quantity (strict)
    # ----------------
    qty_match = re.search(r"\b(1|2|one|two)\b", t)
    if qty_match:
        q = qty_match.group(1)
        quantity = 1 if q in ["1", "one"] else 2
        user.quantity = quantity
        extracted["quantity"] = quantity

    # ----------------
    # Location (only if clear)
    # ----------------
    locations = ["nairobi", "kasarani", "mwiki"]
    if any(loc in t for loc in locations):
        user.location = text.strip()
        extracted["location"] = user.location

    return extracted
