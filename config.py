from openai import OpenAI

client = OpenAI(
    api_key="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",  # 👈 paste FULL key
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-app.onrender.com",
        "X-Title": "WhatsApp Sales Agent"
    }
)

print("🔐 OpenRouter key present:", bool(OPENROUTER_API_KEY))
