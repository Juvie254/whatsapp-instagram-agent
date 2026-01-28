from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse

from agent import process_message
from memory import get_or_create_user
from db import SessionLocal
from models import User

router = APIRouter()

VERIFY_TOKEN = "davii_verify_token_v2"


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
        return PlainTextResponse(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


# -------------------------
# Incoming WhatsApp messages (POST)
# -------------------------
@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    payload = await request.json()

    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]["value"]

        if "messages" not in change:
            return {"status": "ignored"}

        message = change["messages"][0]

        if message["type"] != "text":
            return {"status": "unsupported"}

        phone = ''.join(filter(str.isdigit, message["from"]))
        text = message["text"]["body"]

        # 1️⃣ Get or create user
        user_id = get_or_create_user("whatsapp", phone)

        db = SessionLocal()
        user = db.query(User).get(user_id)

        # 2️⃣ Process message (STATEFUL)
        process_message(user, text)

        db.commit()
        db.close()

        return {"status": "ok"}

    except Exception as e:
        print("Webhook error:", e)
        return {"status": "error"}
