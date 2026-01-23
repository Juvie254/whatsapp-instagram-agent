from fastapi import FastAPI
from contextlib import asynccontextmanager
from webhooks import router as webhook_router
from init_db import init_db
from scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    start_scheduler()
    yield
    # Shutdown
    shutdown_scheduler()

app = FastAPI(
    title="Inbox Conversion Agent",
    lifespan=lifespan
)

app.include_router(webhook_router)

@app.get("/")
async def health():
    return {"status": "ok"}
