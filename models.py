from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    platform = Column(String)
    platform_user_id = Column(String, unique=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    state = Column(String, default="NEW")  

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    direction = Column(String)  # in / out
    content = Column(String)
    intent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    scheduled_for = Column(DateTime)
    sent = Column(Integer, default=0)  # 0 = no, 1 = yes
