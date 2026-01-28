def build_context(user, missing):
    return f"""
Known:
Product: {user.product}
Color: {user.color}
Size: {user.size}
Quantity: {user.quantity}
Location: {user.location}

Missing:
{", ".join(missing) if missing else "None"}

State: {user.state}
"""
