from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db import SessionLocal
from models import FollowUp, User
from send import send_message
from scheduler import scheduler
import pytz

EAT = pytz.timezone("Africa/Nairobi")

FOLLOW_UP_MESSAGES = {
    "ASKING_PRICE": "Just checking 😊 Would you like to order or ask anything else?",
    "INTERESTED": "Still interested? I can help you place the order 👍",
    "OBJECTION": "Let me know if a small discount helps 😊",
}


def schedule_follow_up(user_id: int, platform: str, platform_user_id: str):
    db: Session = SessionLocal()

    followup_time = datetime.now(EAT) + timedelta(minutes=1)

    followup = FollowUp(
        user_id=user_id,
        scheduled_for=followup_time
    )
    db.add(followup)
    db.commit()
    db.refresh(followup)
    db.close()

    scheduler.add_job(
        send_follow_up,
        "date",
        run_date=followup_time,
        misfire_grace_time=300,
        args=[followup.id, platform, platform_user_id]
    )


def send_follow_up(followup_id: int, platform: str, platform_user_id: str):
    db: Session = SessionLocal()

    followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not followup or followup.sent:
        db.close()
        return

    user = db.query(User).filter(User.id == followup.user_id).first()
    if not user:
        db.close()
        return

    msg = FOLLOW_UP_MESSAGES.get(user.state)
    if not msg:
        db.close()
        return

    send_whatsapp_message(platform_user_id, msg)

    followup.sent = True
    user.state = "FOLLOW_UP_SENT"
    db.commit()
    db.close()
