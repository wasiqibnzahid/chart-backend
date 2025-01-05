from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.core.management import call_command
from ...models import LastJobRun, WebsiteCheck
from .run_job import process_urls
from server.constants import PERFORMANCE_METRICS
import time

class Command(BaseCommand):
    help = 'Run scheduled jobs and process pending website checks'

    def handle(self, *args, **kwargs):
        print("Starting scheduled job check...")
        
        # Check if we should run the main jobs
        if LastJobRun.should_run():
            print("Running main jobs...")
            
            # Run all three jobs
            call_command('run_job')
            call_command('local_job')
            call_command('amp_job')
            
            # Update last run time
            LastJobRun.update_last_run()
            print("Main jobs completed")
        
        # Process pending website checks
        while True:
            # Get waiting items in batches of 10
            waiting_checks = WebsiteCheck.objects.filter(
                # waiting or failed
                status__in=['waiting', 'failed']
            ).order_by('created_at')[:1]
            print(f"Waiting checks: {waiting_checks}")
            
            if not waiting_checks:
                print("No pending website checks, shutting down...")
                break
            
            # Process URLs in batch
            urls_to_process = [check.url for check in waiting_checks]
            try:
                # Process URLs and get metrics
                print(f"Processing URLs: {urls_to_process}")
                metrics = process_urls(
                    urls_to_process, 
                    PERFORMANCE_METRICS.copy(),
                    None,  # No site object needed for this case
                    job_type="WEBSITE_CHECK"
                )
                
                # Update each check with its corresponding metrics
                for check, url_metrics in zip(waiting_checks, metrics):
                    try:
                        check.status = 'pending'
                        check.save()
                        # Update all the performance metrics
                        check.note_first_contentful_paint = url_metrics.get('first-contentful-paint', 0)
                        check.note_total_blocking_time = url_metrics.get('total-blocking-time', 0)
                        check.note_speed_index = url_metrics.get('speed-index', 0)
                        check.note_largest_contentful_paint = url_metrics.get('largest-contentful-paint', 0)
                        check.note_cumulative_layout_shift = url_metrics.get('cumulative-layout-shift', 0)
                        check.json_data = url_metrics.get('json_response', {})

                        # Calculate overall score (average of all metrics)
                        check.score = sum(url_metrics.values()) / len(url_metrics) if url_metrics else 0
                        check.status = 'done'
                        check.save()
                        
                        print(f"Processed {check.url} with score {check.score}")
                        
                    except Exception as e:
                        print(f"Error updating check {check.url}: {e}")
                        check.status = 'failed'
                        check.save()
                    
            except Exception as e:
                print(f"Error processing batch: {e}")
                # Mark all checks in batch as pending
                for check in waiting_checks:
                    check.status = 'pending'
                    check.save()
            
            # Small delay between batches
            time.sleep(1)
