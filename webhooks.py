from fastapi import APIRouter, Request, HTTPException
from agent import process_message

router = APIRouter()

VERIFY_TOKEN = "davii_verify_token_123"


# -------------------------
# Webhook verification (Meta GET)
# -------------------------
@router.get("/whatsapp")
async def verify_whatsapp_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


# -------------------------
# Incoming WhatsApp messages (POST)
# -------------------------
@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    payload = await request.json()

    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]

        if message["type"] != "text":
            return {"status": "unsupported"}

        phone = message["from"]
        text = message["text"]["body"]

        # IMPORTANT: match agent signature
        process_message(
            phone=phone,
            text=text
        )

        return {"status": "ok"}

    except Exception as e:
        print("Webhook error:", e)
        return {"status": "error"}
