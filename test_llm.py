from intent import classify_intent
from responder import safe_generate_reply

while True:
    msg = input("You: ")
    intent = classify_intent(msg)
    reply = safe_generate_reply(intent, msg)

    print(f"\nIntent: {intent}")
    print(f"Agent: {reply}\n")
