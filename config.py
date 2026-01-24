from openai import OpenAI
import os

print("🔎 OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("🔎 OPENROUTER_API_KEY =", os.getenv("OPENROUTER_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
print("DEBUG KEY:", os.getenv("OPENROUTER_API_KEY")[:10])
