from django.apps import AppConfig
from django.core.management import call_command
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import threading
import os


def get_next_monday_midnight():
    """Calculate the next Monday at midnight."""
    today = datetime.now()
    days_ahead = 7 - today.weekday()
    next_monday = today + timedelta(days=days_ahead)
    return next_monday.replace(hour=0, minute=0, second=0, microsecond=0)


def run_job():
    call_command("run_job")
    
def amp_job():
    call_command("amp_job")


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

# Removing auto-run since mac will be handling this now
    # def ready(self):
    #     if os.environ.get('RUN_MAIN', None) != 'true':
    #         return
        # thread = threading.Thread(target=self.start_scheduler)
        # thread.daemon = True  # Set the thread as a daemon
        # thread.start()

    def start_scheduler(self):
        scheduler = BackgroundScheduler()
        # run command sequentially
        def run_sequentially():
            run_job()
            amp_job()
            
        # Schedule the job to run once on the next Monday at midnight
        scheduler.add_job(run_sequentially, DateTrigger(
            run_date=get_next_monday_midnight()))

        # Schedule the job to run every week on Monday at midnight after the first run
        scheduler.add_job(run_sequentially, IntervalTrigger(
            weeks=1, start_date=get_next_monday_midnight() + timedelta(weeks=1)))

        # Start the scheduler
        scheduler.start()
