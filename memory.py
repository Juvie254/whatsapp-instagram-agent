from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal
from models import User, Message
from models import FollowUp

def get_or_create_user(platform, platform_user_id):
    db: Session = SessionLocal()

    user = db.query(User).filter_by(
        platform=platform,
        platform_user_id=platform_user_id
    ).first()

    if not user:
        user = User(
            platform=platform,
            platform_user_id=platform_user_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user_id = user.id  # extract ID BEFORE closing session

    user.last_seen = datetime.utcnow()
    db.commit()
    db.close()

    return user_id

def save_message(user_id, direction, content, intent=None):
    db: Session = SessionLocal()
    msg = Message(
        user_id=user_id,
        direction=direction,
        content=content,
        intent=intent
    )
    db.add(msg)
    db.commit()
    db.close()

def cancel_followups(user_id: int):
    db: Session = SessionLocal()
    db.query(FollowUp).filter_by(user_id=user_id, sent=0).delete()
    db.commit()
    db.close()