import os
from openai import OpenAI

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # you set it correctly now

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-app.onrender.com",  # can be any valid URL
        "X-Title": "WhatsApp Instagram Sales Agent"
    }
)

print("🔐 OpenRouter key present:", bool(OPENROUTER_API_KEY))
