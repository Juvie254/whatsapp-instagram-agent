from fastapi import FastAPI
from webhooks import router as webhook_router
from init_db import init_db
from scheduler import start_scheduler

app = FastAPI(title="Inbox Conversion Agent")

@app.on_event("startup")
async def startup():
    init_db()
    start_scheduler()

app.include_router(webhook_router)

@app.get("/")
async def health():
    return {"status": "ok"}
