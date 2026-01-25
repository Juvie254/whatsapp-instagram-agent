import requests
import os

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

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
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-app.onrender.com",
                "X-Title": "WhatsApp Sales Agent"
            },
            json={
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {"role": "system", "content": INTENT_PROMPT},
                    {"role": "user", "content": text}
                ],
                "temperature": 0
            },
            timeout=20
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("🔥 INTENT CLASSIFICATION FAILED:", repr(e))
        return "OTHER"
