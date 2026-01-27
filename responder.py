from config import call_llm

REPLY_PROMPT = """
You are a friendly WhatsApp seller assistant in Kenya.
Reply briefly, warmly, and naturally.
Do not sound like a bot.
Always move the conversation toward purchase.
"""

def generate_reply(intent: str, text: str) -> str:
    result = call_llm(
        model="upstage/solar-pro-3:free",
        messages=[
            {"role": "system", "content": REPLY_PROMPT},
            {"role": "assistant", "content": f"Intent: {intent}"},
            {"role": "user", "content": text}
        ]
    )

    return result["choices"][0]["message"]["content"].strip()
