import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
import concurrent.futures
import threading

from server.models import ImageSite, ImageRecord
from server.helpers import get_lighthouse_mobile_score, write_text_to_file, create_or_update_record, create_empty_records, run_with_timeout
from server.constants import OTHER_RECORD_FILEPATH, PERFORMANCE_METRICS


def process_sitemap(site, semaphore, date):
    with semaphore:
        print(f"Processing sitemap for {site.name}: {site.sitemap_url}")
        try:
            response = requests.get(site.sitemap_url)
            root = ET.fromstring(response.content)

            # Define namespaces
            namespaces = {
                'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                'image': 'http://www.google.com/schemas/sitemap-image/1.1'
            }

            # Initialize metrics
            metrics = PERFORMANCE_METRICS.copy()
            successful_urls = 0

            # Process each URL entry
            for url in root.findall('.//ns:url', namespaces):

                if successful_urls >= 10:  # Only process up to 10 successful URLs
                    break

                loc = url.find('ns:loc', namespaces)
                if loc is None:
                    continue

                # Get all image elements for this URL
                images = url.findall('.//image:image', namespaces)
                if len(images) > 1:  # Only process if there's more than one image
                    print(f"Image count for url {loc.text}: {len(images)}")
                    page_url = loc.text

                    try:
                        # Get Lighthouse score
                        res = run_with_timeout(
                            page_url, "IMAGE JOB", log_file_name=OTHER_RECORD_FILEPATH)

                        if res["performance_score"] != 0:
                            successful_urls += 1
                            for key in metrics:
                                metrics[key] += res[key]

                            print(f"Processed URL {page_url} with {
                                  len(images)} images")

                    except Exception as e:
                        print(f"Error processing URL {page_url}: {str(e)}")
                        continue

            # Calculate averages
            total_urls = max(successful_urls, 1)  # Avoid division by zero
            for key in metrics:
                metrics[key] = metrics[key] / total_urls

            # Multiply performance score by 100 to convert to percentage
            metrics["performance_score"] *= 100

            # Create or update record
            record = create_or_update_record(
                model_class=ImageRecord,
                note_metrics=metrics,
                video_metrics=metrics,  # Using same metrics for both since we're measuring image pages
                site=site,
                date=date,
            )

            print(f"Created record for {site.name} with performance score {
                  metrics['performance_score']}")
            return record

        except Exception as e:
            print(f"Error processing sitemap for {site.name}: {str(e)}")
            raise e
            write_text_to_file(f"Error processing sitemap for {
                               site.name}: {str(e)}", OTHER_RECORD_FILEPATH)


class Command(BaseCommand):
    help = 'Process image sitemaps and calculate Lighthouse scores'

    def handle(self, *args, **kwargs):
        sites = ImageSite.objects.all()
        semaphore = threading.Semaphore(1)
        records_to_create = []
        today = datetime.today()
        monday_of_current_week = today - timedelta(days=today.weekday())
        date = monday_of_current_week.date()
        create_empty_records(sites, ImageRecord)

        ImageRecord.objects.bulk_create(records_to_create)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_site = {executor.submit(
                process_sitemap, site, semaphore, date): site for site in sites}
            for future in concurrent.futures.as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing site {site.name}: {str(e)}")
                    raise e
                    write_text_to_file(f"Error processing site {site.name}: {
                        str(e)}", OTHER_RECORD_FILEPATH)
