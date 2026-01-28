from llm import call_llm

REPLY_PROMPT = """
You are a friendly WhatsApp seller assistant in Kenya.
Reply briefly, warmly, and naturally.
Do not sound like a bot.
Always move the conversation toward purchase.
"""

def generate_reply(intent: str, text: str) -> str:
    return call_llm([
        {"role": "system", "content": REPLY_PROMPT},
        {"role": "assistant", "content": f"Intent: {intent}"},
        {"role": "user", "content": text}
    ])
def safe_generate_reply(intent, text):
    try:
        return generate_reply(intent, text)
    except Exception as e:
        print("🔥 REPLY FAILED:", e)
        return "Hi 😊 I’m here to help. Could you tell me what you’re looking for?"
