from llm import call_llm

INTENT_PROMPT = """
Classify the message into exactly ONE of these categories:
ASK_PRICE
INTEREST
OBJECTION
BUY
OTHER

Return ONLY the category name.
"""

def classify_intent(text: str) -> str:
    try:
        reply = call_llm([
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": text}
        ])
        return reply
    except Exception as e:
        print("🔥 INTENT FAILED:", e)
        return "OTHER"
