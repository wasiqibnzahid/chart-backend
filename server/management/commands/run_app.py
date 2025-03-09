from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.core.management import call_command
from ...models import LastJobRun, WebsiteCheck
from .run_job import process_urls
from ...helpers import get_lighthouse_mobile_score, run_with_timeout
from ...utils import upload_to_s3
from server.constants import PERFORMANCE_METRICS
import time
import uuid


class Command(BaseCommand):
    help = 'Run scheduled jobs and process pending website checks'

    def handle(self, *args, **kwargs):
        print("Starting scheduled job check...")

        # Check if we should run the main jobs
        if LastJobRun.should_run():
            print("Running main jobs...")

            # Get current job state
            last_job = LastJobRun.objects.get(id=1)
            job_sequence = ['run_job', 'local_job', 'amp_job', 'image_job']
            
            # Find next job to run
            current_job = getattr(last_job, 'current_job', None)
            is_last_job = False
            print(f"Last job run: {current_job}")
            if not current_job:
                current_job = job_sequence[0]
            elif current_job in job_sequence:
                next_index = job_sequence.index(current_job) + 1
                if next_index < len(job_sequence):
                    current_job = job_sequence[next_index]
                else:
                    # All jobs completed
                    is_last_job = True
                    # LastJobRun.update_last_run()
                    # Reset current_job to start fresh next time
                    last_job.current_job = None
                    last_job.save()
                    print("All jobs completed")
                    return

            # Run current job
            print(f"Running {current_job}...")
            # call_command(current_job)
            print(f"{current_job} completed")

            # Save state and restart
            if is_last_job:
                last_job.current_job = None
            else:
                last_job.current_job = current_job
            last_job.save()
            # import os
            # os.system('sudo reboot')

        # Process pending website checks
        while True:
            # Get waiting items in batches of 10
            waiting_check = WebsiteCheck.objects.filter(
                status__in=['waiting', 'pending']
            ).first()
            print(f"Waiting checks: {waiting_check}")

            if not waiting_check:
                print("No pending website checks, shutting down...")
                break

            try:
                # Process URLs and get metrics
                print(f"Processing URL: {waiting_check.url}")
                waiting_check.status = 'pending'
                waiting_check.save()

                # Generate unique filename for S3
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                filename = f"lighthouse/{timestamp}_{unique_id}.json"

                url_metrics = run_with_timeout(
                    waiting_check.url,
                    job_type="WEBSITE_CHECK",
                    should_save_json=True
                )

                try:
                    if url_metrics.get('performance_score', 0) == 0:
                        raise Exception("Performance score is 0")

                    # Upload JSON to S3
                    if 'json_response' in url_metrics:
                        s3_url = upload_to_s3(url_metrics['json_response'], filename)
                        print(f"Uploaded to S3: {s3_url}")
                        if s3_url:
                            waiting_check.json_url = s3_url

                    # Update metrics
                    waiting_check.metrics = {
                        "performance_score": url_metrics["performance_score"],
                        "first_contentful_paint": url_metrics["first_contentful_paint"],
                        "total_blocking_time": url_metrics["total_blocking_time"],
                        "speed_index": url_metrics["speed_index"],
                        "largest_contentful_paint": url_metrics["largest_contentful_paint"],
                        "cumulative_layout_shift": url_metrics["cumulative_layout_shift"],
                    }
                    waiting_check.status = 'done'
                    waiting_check.save()

                    print(f"Processed {waiting_check.url} successfully")

                except Exception as e:
                    print(f"Error updating check {waiting_check.url}: {e}")
                    waiting_check.status = 'failed'
                    waiting_check.save()

            except Exception as e:
                print(f"Error processing URL: {e}")
                waiting_check.status = 'failed'
                waiting_check.save()

            # Small delay between checks
            time.sleep(1)
