from config import call_llm

res = call_llm(
    model="test",
    messages=[
        {"role": "system", "content": "You are friendly."},
        {"role": "user", "content": "Say hello again."}
    ]
)

print(res["choices"][0]["message"]["content"])
