from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal
from models import User, Message, FollowUp

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

    user.last_seen = datetime.utcnow()
    db.commit()

    return user, db
