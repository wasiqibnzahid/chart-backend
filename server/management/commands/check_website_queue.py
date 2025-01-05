from django.core.management.base import BaseCommand
import time
import threading
from django.db import connection
from ...models import WebsiteCheck

def notify_waiting_items():
    """Function to check for waiting items and notify"""
    try:
        waiting_count = WebsiteCheck.objects.filter(status='waiting').count()
        if waiting_count > 0:
            print(f"Found {waiting_count} items waiting to be processed")
            return True
        return False
    except Exception as e:
        print(f"Error checking waiting items: {e}")
        return False

class Command(BaseCommand):
    help = 'Continuously check for websites in waiting status'

    def handle(self, *args, **kwargs):
        def check_queue():
            while True:
                try:
                    # Close any stale database connections
                    connection.close()
                    
                    # Just check for waiting items
                    notify_waiting_items()
                    
                    # Wait for 5 minutes
                    time.sleep(300)  # 300 seconds = 5 minutes
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error in check_queue: {str(e)}')
                    )
                    # Wait a bit before retrying after error
                    time.sleep(30)

        # Start the checker in a separate thread
        checker_thread = threading.Thread(target=check_queue)
        checker_thread.daemon = True
        checker_thread.start()
        
        self.stdout.write(
            self.style.SUCCESS('Started website queue checker')
        )
        
        # Keep the main thread running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.SUCCESS('Stopping website queue checker...')
            ) 