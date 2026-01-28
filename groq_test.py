import os
from groq import Groq

print("🔑 GROQ KEY PRESENT:", bool(os.getenv("GROQ_API_KEY")))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are a friendly human assistant."},
        {"role": "user", "content": "Say hello like a real person."}
    ]
)

print("🤖 GROQ RESPONSE:")
print(response.choices[0].message.content)
