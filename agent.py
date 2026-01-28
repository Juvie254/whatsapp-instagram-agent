from intent import detect_intent
from policy import should_respond, next_state
from memory import save_message
from messaging import send_whatsapp_message
from followup import schedule_follow_up
from handoff import handoff_to_human
from groq import Groq

client = Groq()

def call_llm(messages):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.6
    )
    return response.choices[0].message.content


def process_message(user, text):
    # 1️⃣ Save incoming message
    save_message(user.id, "in", text)

    # 2️⃣ Detect intent
    intent = detect_intent(text)

    # 3️⃣ Policy check (CRITICAL)
    if not should_respond(user.state, intent):
        print("🛑 Policy blocked response")
        return None

    # 4️⃣ State transition
    new_state = next_state(user.state, intent)
    user.state = new_state

    # 5️⃣ Hard rules (NO LLM)
    if intent == "BUY":
        handoff_to_human(user)
        return None

    # 6️⃣ LLM reply
    system_prompt = f"""
You are a WhatsApp sales assistant.
User state: {user.state}
Intent: {intent}

Rules:
- Be short
- Be friendly
- Do not push if user is not interested
"""

    reply = call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ])

    # 7️⃣ Send reply
    send_whatsapp_message(user.platform_user_id, reply)

    # 8️⃣ Save outgoing message
    save_message(user.id, "out", reply, intent)

    # 9️⃣ Follow-up logic
    if intent in ["ASK_PRICE", "INTEREST"]:
        schedule_follow_up(user.id, user.platform, user.platform_user_id)

    return reply

