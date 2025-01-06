from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.core.management import call_command
from ...models import LastJobRun, WebsiteCheck
from .run_job import process_urls
from ...helpers import get_lighthouse_mobile_score
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
            # TODO: Uncomment this
            # call_command('run_job')
            # call_command('local_job')
            # call_command('amp_job')

            # Update last run time
            LastJobRun.update_last_run()
            print("Main jobs completed")

        # Process pending website checks
        while True:
            # Get waiting items in batches of 10
            waiting_check = WebsiteCheck.objects.filter(
                status__in=['waiting', 'pending']
            ).first()
            print(f"Waiting checks: {waiting_check.url}")

            if not waiting_check:
                print("No pending website checks, shutting down...")
                break

            # Process URLs in batch
            # urls_to_process = [waiting_check.url]
            urls_to_process = 'https://www.tvazteca.com/aztecauno/lo-que-callamos-las-mujeres/rocio-un-llanto-en-silencio'

            try:
                # Process URLs and get metrics
                print(f"Processing URLs: {urls_to_process}")
                waiting_check.status = 'pending'
                waiting_check.save()
                url_metrics = get_lighthouse_mobile_score(
                    urls_to_process,
                    job_type="WEBSITE_CHECK"
                )

                # Update each check with its corresponding metrics

                try:

                    print(f"CHECK IS {waiting_check}")
                    # Update all the performance metrics
                    if url_metrics.get(
                            'performance_score', 0) == 0:
                        raise Exception("Performance score is 0")
                    waiting_check.metrics = {
                        "performance_score": url_metrics["performance_score"],
                        "first_contentful_paint": url_metrics["first_contentful_paint"],
                        "total_blocking_time": url_metrics["total_blocking_time"],
                        "speed_index": url_metrics["speed_index"],
                        "largest_contentful_paint": url_metrics["largest_contentful_paint"],
                        "cumulative_layout_shift": url_metrics["cumulative_layout_shift"],
                    }
                    waiting_check.json_data = url_metrics["json_response"]
                    # set all items where url is same their json_data to {}
                    WebsiteCheck.objects.filter(
                        url=waiting_check.url).update(json_data={})
                    waiting_check.status = 'done'
                    waiting_check.save()

                    print(f"Processed {waiting_check.url} with score {
                        waiting_check.metrics}")

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
