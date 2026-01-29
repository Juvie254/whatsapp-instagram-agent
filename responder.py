from llm import call_llm

REPLY_PROMPT = """
You are a WhatsApp sales assistant in Kenya.

State: {state}

Known details:
{known}

Missing details:
{missing}

Rules:
- Replies under 2 sentences.
- Never ask for known information.
- Ask only ONE missing detail if any.
- If READY_TO_CONFIRM, confirm the order clearly.
- If DISENGAGED, politely stop selling.
- Sound human, calm, and confident.
- Do not oversell. Respond naturally like a real person.
- If the user is vague, respond with a short, open-ended question.
"""

def generate_reply(intent, text, context, state):
    # 🟢 Human greeting override
    if intent == "GREETING" and state == "NEW":
        return "Hi 😊\nHow can I help you today?"

    system_prompt = REPLY_PROMPT.format(
        state=state,
        known=context["known"] or "None",
        missing=", ".join(context["missing"]) if context["missing"] else "None"
    )

    reply = call_llm(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
    )

    return reply.strip()


def safe_generate_reply(intent, text, context, state):
    try:
        return generate_reply(intent, text, context, state)
    except Exception as e:
        print("🔥 REPLY FAILED:", e)
        return "Hi 😊 How can I help you?"

