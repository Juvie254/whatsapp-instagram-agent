from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def add_jobs():
    # Example dummy job (keeps scheduler alive)
    scheduler.add_job(
        lambda: None,
        trigger="interval",
        seconds=60,
        id="keep_alive",
        replace_existing=True
    )

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
