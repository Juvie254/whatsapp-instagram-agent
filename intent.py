from config import call_llm

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
        result = call_llm(
            model="upstage/solar-pro-3:free",
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("🔥 INTENT CLASSIFICATION FAILED:", repr(e))
        return "OTHER"
