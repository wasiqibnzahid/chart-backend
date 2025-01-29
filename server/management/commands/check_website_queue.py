from django.core.management.base import BaseCommand
import time
import threading
from django.db import connection
from ...models import WebsiteCheck, LastJobRun
import requests

LAMBDA_URL = "https://hpuyeonhb3mctgalziaie3py7m0vnqfk.lambda-url.us-east-1.on.aws/"

def notify_waiting_items():
    """Function to check for waiting items and notify Lambda"""
    try:
        waiting_count = WebsiteCheck.objects.filter(status='waiting').count()
        if waiting_count > 0 or LastJobRun.should_run():
            print(f"Found {waiting_count} items waiting to be processed")
            try:
                # Make request to Lambda
                response = requests.get(LAMBDA_URL)
                print(f"Lambda notification response: {response.text}")
                return True
            except Exception as e:
                print(f"Error notifying Lambda: {e}")
                return False
        else:
            print("No waiting items found")
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
                    
                    # Check for waiting items and notify Lambda if found
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