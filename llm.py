import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(messages, model="openai/gpt-oss-120b"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
