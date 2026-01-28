from llm import call_llm

REPLY_PROMPT = """
You are a WhatsApp sales assistant in Kenya.

Rules:
- Replies under 2 sentences.
- Never ask for known information.
- Ask only ONE missing detail if any.
- If READY_TO_CONFIRM, confirm the order.
- If DISENGAGED, politely stop selling.
- Sound human and confident.
"""

def generate_reply(intent, text, context, state):
    result = call_llm(
        messages=[
            {"role": "system", "content": REPLY_PROMPT},
            {"role": "assistant", "content": context},
            {"role": "assistant", "content": f"Intent: {intent}"},
            {"role": "assistant", "content": f"State: {state}"},
            {"role": "user", "content": text},
        ]
    )

    return result.strip()

def safe_generate_reply(intent, text):
    try:
        return generate_reply(intent, text)
    except Exception as e:
        print("🔥 REPLY FAILED:", e)
        return "Hi 😊 I’m here to help. Could you tell me what you’re looking for?"
