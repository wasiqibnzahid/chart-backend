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
            # filter(
            #     status='waiting'
            # )
            waiting_check = WebsiteCheck.objects.first()
            print(f"Waiting checks: {waiting_check}")

            if not waiting_check:
                print("No pending website checks, shutting down...")
                break

            # Process URLs in batch
            # urls_to_process = [waiting_check.url]
            urls_to_process = ['https://www.aztecayucatan.com/clima/atencion-toda-de-baja-presion-aumenta-su-probabilidad-de-formar-el-ciclon-patty-frente-a-yucatan']

            try:
                # Process URLs and get metrics
                print(f"Processing URLs: {urls_to_process}")
                url_metrics = process_urls(
                    urls_to_process,
                    PERFORMANCE_METRICS.copy(),
                    None,  # No site object needed for this case
                    job_type="WEBSITE_CHECK"
                )

                # Update each check with its corresponding metrics

                try:
                    waiting_check.status = 'pending'
                    print(f"CHECK IS {waiting_check}")
                    waiting_check.save()
                    # Update all the performance metrics
                    print(f" metrics are {url_metrics}")
                    waiting_check.note_first_contentful_paint = url_metrics.get(
                        'first-contentful-paint', 0)
                    waiting_check.note_total_blocking_time = url_metrics.get(
                        'total-blocking-time', 0)
                    waiting_check.note_speed_index = url_metrics.get(
                        'speed-index', 0)
                    waiting_check.note_largest_contentful_paint = url_metrics.get(
                        'largest-contentful-paint', 0)
                    waiting_check.note_cumulative_layout_shift = url_metrics.get(
                        'cumulative-layout-shift', 0)
                    waiting_check.json_data = url_metrics.get(
                        'json_response', {})

                    # Calculate overall score (average of all metrics)
                    waiting_check.score = sum(url_metrics.values()) / \
                        len(url_metrics) if url_metrics else 0
                    waiting_check.status = 'done'
                    waiting_check.save()

                    print(f"Processed {waiting_check.url} with score {
                        waiting_check.score}")

                except Exception as e:
                    print(f"Error updating check {waiting_check.url}: {e}")
                    waiting_check.status = 'failed'
                    waiting_check.save()

            except Exception as e:
                print(f"Error processing batch: {e}")
                # Mark all checks in batch as pending
                waiting_check.status = 'failed'
                waiting_check.save()

            # Small delay between batches
            time.sleep(1)
