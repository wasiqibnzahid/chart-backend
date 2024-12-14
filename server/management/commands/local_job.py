import random
import subprocess
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import concurrent.futures
import json
import os
import threading

from server.constants import OTHER_RECORD_FILEPATH, PERFORMANCE_METRICS
from server.helpers import create_empty_records, create_or_update_record, create_record_if_not_exists, process_urls, write_text_to_file
from ...models import LocalErrorLog, LocalRecord, LocalSite
from server.local_data.local_data import azteca_columns_raw
from .run_job import fetch_data, get_latest_urls, get_sorted_rss_items

def process_site(site: LocalSite, semaphore):
    with semaphore:
        print(f"Init for site {site.name} {site.sitemap_url}, note: {
              site.note_sitemap_url} video: {site.video_sitemap_url}")
        today = datetime.today()
        monday_of_current_week = today - timedelta(days=today.weekday())
        date = monday_of_current_week.date()
        try:
            note_sitemap_url = site.sitemap_url
            video_sitemap_url = site.sitemap_url
            if site.note_sitemap_url:
                note_sitemap_url = site.note_sitemap_url
            if site.video_sitemap_url:
                video_sitemap_url = site.video_sitemap_url
            nota_xml = fetch_data(note_sitemap_url)
            video_xml = fetch_data(video_sitemap_url)
            extracted_video_urls = site.video_urls or []
            extracted_nota_urls = site.note_urls or []
            extracted_nota_urls_inner = get_latest_urls(
                nota_xml, is_xml="html" not in note_sitemap_url)
            extracted_video_urls_inner = get_latest_urls(
                video_xml, is_xml="html" not in video_sitemap_url)
            extracted_video_urls.extend(extracted_video_urls_inner)

            if len(extracted_nota_urls_inner) == 0:
                log = LocalErrorLog(message=f"Sitemap returned 0 urls: {
                               note_sitemap_url}")
                log.save()
            if len(extracted_video_urls_inner) == 0:
                log = LocalErrorLog(message=f"Sitemap returned 0 urls: {
                               video_sitemap_url}")
                log.save()

            extracted_nota_urls.extend(extracted_nota_urls_inner)
            extracted_video_urls.extend(extracted_video_urls_inner)
            print(f"For company {site.name} the note urls are "
                  f"{len(extracted_nota_urls)} and video are {len(extracted_video_urls_inner)}")
            
            # Process Note Urls
            note_metrics = process_urls(extracted_nota_urls, PERFORMANCE_METRICS.copy(), site, job_type="LOCAL JOB", log_file_name=OTHER_RECORD_FILEPATH)
            
            # Process video URLs
            video_metrics = process_urls(extracted_video_urls, PERFORMANCE_METRICS.copy(), site, url_type="video", job_type="LOCAL JOB", log_file_name=OTHER_RECORD_FILEPATH)
            
            print(f"SCORE IS {site.name} NOTE: {note_metrics} VIDEO: {video_metrics}")
            
            record = create_or_update_record(
                model_class=LocalRecord, 
                note_metrics=note_metrics,
                video_metrics=video_metrics,
                site=site,
                date=date,
            )
            
            write_text_to_file(f"RECORD IS {record.name} NOTE: {record.note_value} VIDEO: {record.video_value}")
            return record

        except Exception as e:
            # Log the exception with a more detailed message
            print(f"Exception occurred while processing site '{site.name}' on {date}: {e}")
            
            # Attempt to create the record if not already exists
            record, created = create_record_if_not_exists(
                model_class=LocalRecord,
                site=site,
                date=date,
            )
            
            # Log the outcome of the create operation after an exception
            if created:
                write_text_to_file(
                    f"Exception occurred: New Local Record created for site '{record.name}' with NOTE: {record.note_value} and VIDEO: {record.video_value} due to an error.",
                    filename=OTHER_RECORD_FILEPATH
                )
            else:
                write_text_to_file(
                    f"Exception occurred: Existing Local Record found for site '{record.name}' with NOTE: {record.note_value} and VIDEO: {record.video_value}. No changes were made due to an error.",
                    filename=OTHER_RECORD_FILEPATH
                )
                
            return record


def run_job():

    sites = LocalSite.objects.all()
    create_empty_records(sites, LocalRecord)
    records = []
    semaphore = threading.Semaphore(4)
    print(f"SIOTES ARE {sites}")
    today = datetime.today()
    monday_of_current_week = today - timedelta(days=today.weekday())
    date = monday_of_current_week.date()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print(f"STARINT PROCESSING SITE A")
        future_to_site = {executor.submit(
            process_site, site, semaphore): site for site in sites}
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            result = future.result()  # Get the result of the future
            records.append(result)
            # print(f"Processed site {site}: Result = {result}")
    print(f"STATUS IS DONE")
    # LocalRecord.objects.filter(date=date).delete()
    if records:
        for record in records:
            write_text_to_file(f"RECORD IS {record.name} {
                               record.note_value} {record.video_value}")
    # LocalRecord.objects.bulk_create(records)

class Command(BaseCommand):
    help = 'Run a long function in a separate thread'

    def handle(self, *args, **kwargs):
        print(f"SSTARTING")
        run_job()
