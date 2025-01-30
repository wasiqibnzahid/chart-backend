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

            # Run all three jobs
            call_command('run_job')
            print("run_job completed")
            call_command('local_job')
            print("local_job completed")
            call_command('amp_job')
            print("amp_job completed")
            call_command('image_job')
            print("image_job completed")
            # Update last run time
            # LastJobRun.update_last_run()
            print("Main jobs completed")

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
