from django.apps import AppConfig
from django.core.management import call_command
import threading

class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        # Prevent running twice in development
        import os
        if os.environ.get('RUN_MAIN'):
            def start_checker():
                call_command('check_website_queue')

            thread = threading.Thread(target=start_checker)
            thread.daemon = True
            thread.start()
