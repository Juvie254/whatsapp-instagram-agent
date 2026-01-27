from openai import OpenAI
import os
import requests


#client = OpenAI(
    #api_key="sk-or-#v1-9d2e2b1a38710c68dcfb0df5e57b66f0d77b2c8ad7daa49a3c8bbc9f37011e02",  # 👈 paste FULL key
    #base_url="https://openrouter.ai/api/v1",
    #default_headers={
        #"HTTP-Referer": "https://your-app.onrender.com",
        #"X-Title": "WhatsApp Sales Agent"
    #}
#)


#OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#if not OPENROUTER_API_KEY:
    #raise RuntimeError("❌ OPENROUTER_API_KEY not set")

#client = OpenAI(
    #api_key=OPENROUTER_API_KEY,
    #base_url="https://openrouter.ai/api/v1",
    #default_headers={
        #"HTTP-Referer": "http://localhost",  # REQUIRED
        #"X-Title": "WhatsApp Sales Agent"    # REQUIRED
    #}
#)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY not set")

def call_llm(model: str, messages: list):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # 🔑 THESE TWO ARE CRITICAL
        "HTTP-Referer": "http://localhost",
        "X-Title": "WhatsApp Agent"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload)

    # 🔍 DEBUG ON FAILURE
    if response.status_code != 200:
        print("❌ OpenRouter response:", response.status_code)
        print(response.text)

    response.raise_for_status()
    return response.json()
