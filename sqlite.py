from db import SessionLocal
from models import User, Message

db = SessionLocal()
print(db.query(User).all())
print(db.query(Message).all())
