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
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        intent = result["choices"][0]["message"]["content"].strip().upper()
        return intent
    except Exception as e:
        print("🔥 INTENT CLASSIFICATION FAILED:", repr(e))
        return "OTHER"
