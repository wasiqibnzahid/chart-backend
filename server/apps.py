from django.apps import AppConfig
import time
from django.core.management import call_command
import threading


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    # def ready(self):
    #     threading.Thread(target=self.run_job, daemon=True).start()

    # def run_job(self):
    #     print(f"RUNNING")
    #     call_command("run_job")
    #     while True:
    #         print(f"RUNNING sleeping")
    #         time.sleep(3600 * 48)  # Sleep for 2 days
    #         call_command('run_job')
