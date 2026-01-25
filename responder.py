from config import client

#client = OpenAI(api_key=OPENAI_API_KEY)

REPLY_PROMPT = """
You are a friendly WhatsApp seller assistant in Kenya.
Reply briefly, warmly, and naturally.
Do not sound like a bot.
Always move the conversation toward purchase.
"""

def generate_reply(intent: str, text: str) -> str:
    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[
            {"role": "system", "content": REPLY_PROMPT},
            {"role": "assistant", "content": f"Intent: {intent}"},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
