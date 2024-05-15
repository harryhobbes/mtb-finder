import os

import click

from app.deal import refresh_helper
from flask_apscheduler import APScheduler

scheduler = APScheduler()

@click.command('list-tasks')
def list_tasks():
    """List all scheduled tasks"""
    for job in scheduler.get_jobs():
        print(job)

def init_app(app):    

    app.cli.add_command(list_tasks)    
    
    scheduler.init_app(app)
    scheduler.start()
    
    # Add a scheduler to run deal refresh on a set interval
    scheduler.add_job(
        func=run_scheduled_tasks,
        trigger='cron',
        minute=os.getenv("CRON_INTERVAL",59),
        id="refresh_deals",
    )
    
# Add a scheduler to run deal refresh on a set interval
def run_scheduled_tasks():
    with scheduler.app.app_context():
        refresh_helper()