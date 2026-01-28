from config import call_llm

REPLY_PROMPT = """
You are a friendly WhatsApp seller assistant in Kenya.

Rules:
- Reply briefly and warmly
- Sound human, not robotic
- Be persuasive but respectful
- Always guide the user toward a purchase or next step
"""

def generate_reply(intent: str, text: str) -> str:
    try:
        result = call_llm(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": REPLY_PROMPT},
                {"role": "assistant", "content": f"Detected intent: {intent}"},
                {"role": "user", "content": text}
            ]
        )

        reply = result["choices"][0]["message"]["content"].strip()
        return reply

    except Exception as e:
        print("🔥 REPLY GENERATION FAILED:", repr(e))
        return ""
