import os

from app.deal import refresh_helper
from flask_apscheduler import APScheduler

scheduler = APScheduler()

def init_app(app):    
    
    scheduler.init_app(app)
    scheduler.start()
    
    # Add a scheduler to run deal refresh on a set interval
    scheduler.add_job(
        func=run_scheduled_tasks,
        trigger='cron',
        minute=os.getenv("CRON_INTERVAL",60),
        id="refresh_deals",
    )
    
# Add a scheduler to run deal refresh on a set interval
def run_scheduled_tasks():
    with scheduler.app.app_context():
        refresh_helper()