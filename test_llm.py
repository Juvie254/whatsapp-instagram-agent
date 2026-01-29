from intent import classify_intent
from responder import safe_generate_reply

# Mock user context (same shape as build_context)
def mock_context():
    return {
        "known": {
            "product": "jacket",
            "color": "black"
        },
        "missing": ["size", "quantity", "location"],
        "state": "DISCOVERY",
        "rules": []
    }

while True:
    msg = input("You: ")
    intent = classify_intent(msg)

    context = mock_context()
    state = context["state"]

    reply = safe_generate_reply(intent, msg, context, state)

    print(f"\nIntent: {intent}")
    print(f"Agent: {reply}\n")
