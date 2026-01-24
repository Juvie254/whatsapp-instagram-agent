from config import client
import os

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
        response = client.chat.completions.create(
            model="mistralai/devstral-2512:free",
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("🔐 OpenRouter key present:", bool(os.getenv("OPENROUTER_API_KEY")))
        print("🔥 INTENT CLASSIFICATION FAILED:", repr(e))
        return "OTHER"
