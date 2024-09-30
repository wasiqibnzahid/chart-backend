from django.apps import AppConfig
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from apscheduler.triggers.interval import IntervalTrigger
import calendar
import threading
import os
from datetime import datetime, timedelta


def get_next_monday_midnight():
    today = datetime.now()
    today = today.replace(minute=59)
    print(f"SCHEDULED FOR {today}")
    return today
    # days_ahead = 0 - today.weekday() if today.weekday() <= 0 else 7 - today.weekday()
    # next_monday = today + timedelta(days=days_ahead)
    # return next_monday.replace(hour=0, minute=0, second=0, microsecond=0)


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

#     def ready(self, *args, **options):
#         print(f"THE ENV IS {os.environ.get("RUN_MAIN", None)}")
#         if os.environ.get('RUN_MAIN', None) != 'true':
#             return
#         # Calculate the time for the next Monday at 12 AM
#         now = datetime.now()
#         monday = now + timedelta(days=(calendar.MONDAY - now.weekday()) %
#                                  7, weeks=(now.weekday() == calendar.MONDAY))
#         target_time = datetime(monday.year, monday.month, monday.day, 12, 0)

#         if target_time > now:
#             delay = (target_time - now).total_seconds()
#             self.stdout.write(f"First run scheduled for {
#                 target_time} (delay: {delay:.2f} seconds)")
#             threading.Timer(delay, self.background_job).start()
#         else:
#             self.stdout.write(
#                 "Current time is past Monday 12 AM. Starting job immediately.")
#             self.background_job()
#         # Define the function for the background job

#     def background_job(self):
#         # Your background job logic here
#         print("Running background job!")

#         # Schedule the next execution for the following Monday
#         self.schedule_next_run()

#     # Schedule the initial execution

#     # Schedule the next execution within the background job function
#     def schedule_next_run(self):
#         next_monday = target_time + timedelta(days=7)
#         delay = (next_monday - datetime.now()).total_seconds()
#         threading.Timer(delay, background_job).start()
#     # scheduler = BackgroundScheduler()

#     # # Ensure the scheduler stops with the main thread
#     # scheduler.daemonic = True

#     # # Get the next Monday midnight
#     # next_monday_midnight = get_next_monday_midnight()

#     # # Add job to scheduler with interval trigger, starting at next Monday midnight and running every 7 days
#     # scheduler.add_job(
#     #     self.run_job,
#     #     trigger=IntervalTrigger(seconds=6),
#     #     start_date=next_monday_midnight
#     # )

#     # # Start the scheduler
#     # scheduler.start()


# def run_job(self):
#     print(f"RUNNING")
#     # call_command("run_job")
