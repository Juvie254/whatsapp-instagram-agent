from openai import OpenAI
from config import client

#client = OpenAI(api_key=OPENAI_API_KEY)

INTENT_PROMPT = """
Classify the message into exactly one category:
GREETING, PRICE, AVAILABILITY, DELIVERY, READY_TO_BUY, NOT_INTERESTED, OTHER.
Return only the category.
"""

def classify_intent(text: str) -> str:
    response = client.chat.completions.create(
        model="mistralai/devstral-2512:free",
        messages=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()
