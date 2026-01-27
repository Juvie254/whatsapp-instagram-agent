from config import call_llm

if __name__ == "__main__":
    result = call_llm(
        model="arcee-ai/trinity-large-preview:free",
        messages=[
            {"role": "user", "content": "Say OK only"}
        ]
    )

    print("LLM response:", result["choices"][0]["message"]["content"])
