from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    platform = Column(String, nullable=False)
    platform_user_id = Column(String, unique=True, nullable=False)

    # Conversation control
    state = Column(String, default="NEW")

    # 🧠 Structured memory
    product = Column(String, nullable=True)
    color = Column(String, nullable=True)
    size = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    location = Column(String, nullable=True)

    last_seen = Column(DateTime, default=datetime.utcnow)
