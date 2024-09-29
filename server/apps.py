from django.apps import AppConfig
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from apscheduler.triggers.interval import IntervalTrigger

import threading
import os
from datetime import datetime, timedelta


def get_next_monday_midnight():
    today = datetime.now()
    today.replace(minute=today.minute + 3)
    print(f"SCHEDULED FOR {today}")
    return today
    # days_ahead = 0 - today.weekday() if today.weekday() <= 0 else 7 - today.weekday()
    # next_monday = today + timedelta(days=days_ahead)
    # return next_monday.replace(hour=0, minute=0, second=0, microsecond=0)


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        scheduler = BackgroundScheduler()

        # Ensure the scheduler stops with the main thread
        scheduler.daemonic = True

        # Get the next Monday midnight
        next_monday_midnight = get_next_monday_midnight()

        # Add job to scheduler with interval trigger, starting at next Monday midnight and running every 7 days
        scheduler.add_job(
            self.run_job,
            trigger=IntervalTrigger(weeks=1),
            start_date=next_monday_midnight
        )

        # Start the scheduler
        scheduler.start()

    def run_job(self):
        print(f"RUNNING")
        call_command("run_job")
        while True:
            print(f"RUNNING sleeping")
            time.sleep(3600 * 48)  # Sleep for 2 days
            call_command('run_job')
