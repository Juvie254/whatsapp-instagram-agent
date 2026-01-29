from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal
from models import User

def get_or_create_user(platform: str, platform_user_id: str):
    """
    Returns (user, db_session)
    Caller must commit & close session.
    """
    db: Session = SessionLocal()

    user = db.query(User).filter_by(
        platform=platform,
        platform_user_id=platform_user_id
    ).first()

    if not user:
        user = User(
            platform=platform,
            platform_user_id=platform_user_id,
            state="NEW"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Update last_seen timestamp
    user.last_seen = datetime.utcnow()
    db.commit()

    return user, db

