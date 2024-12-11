import subprocess
import random
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import concurrent.futures
import json
import os
import threading

from server.constants import OTHER_RECORD_FILEPATH, PERFORMANCE_METRICS
from server.helpers import create_or_update_record, create_record_if_not_exists, process_urls, write_text_to_file
from ...models import ErrorLog, Record, Site
from ...generate_reports import fetch_data, get_latest_urls, get_sorted_rss_items


def process_site(site: Site, semaphore):
    with semaphore:
        print(f"Init for site {site.name} {site.sitemap_url}, note: {site.note_sitemap_url} video: {site.video_sitemap_url}")
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
            extracted_video_urls = site.video_urls
            extracted_nota_urls = site.note_urls
            if site.name == 'El Heraldo':
                extracted_video_urls_inner, extracted_nota_urls_inner = get_latest_urls(
                    site.sitemap_url, is_xml=False)
            elif site.name == "AS":
                extracted_nota_urls_inner = get_sorted_rss_items(
                    site.note_sitemap_url)
                extracted_video_urls_inner = get_sorted_rss_items(
                    site.video_sitemap_url)
            else:
                extracted_nota_urls_inner = get_latest_urls(
                    nota_xml, is_xml="html" not in note_sitemap_url)
                extracted_video_urls_inner = get_latest_urls(
                    video_xml, is_xml="html" not in video_sitemap_url)
                if (site.name == "NY Times"):
                    video_xml = fetch_data(extracted_video_urls_inner[0])
                    extracted_video_urls_inner = get_latest_urls(
                        video_xml, is_xml=True)

            if site.name == "Milenio" or site.name == "El Universal":
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "video" not in item]
                extracted_video_urls_inner = [
                    item for item in extracted_video_urls_inner if "video" in item]
            if site.name == "Infobae" or site.name == "AS":
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "video" not in item]
            if site.name == "Terra":
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "nacionales" in item]
                extracted_video_urls_inner = [
                    item for item in extracted_video_urls_inner if "entretenimiento" in item]
            extracted_nota_urls.extend(extracted_nota_urls_inner)
            extracted_video_urls.extend(extracted_video_urls_inner)
            
            if len(extracted_nota_urls_inner) == 0:
                log = ErrorLog(message=f"Sitemap returned 0 urls: { note_sitemap_url}")
                log.save()
            if len(extracted_video_urls_inner) == 0:
                log = ErrorLog(message=f"Sitemap returned 0 urls: {video_sitemap_url}")
                log.save()

            extracted_nota_urls.extend(extracted_nota_urls_inner)
            extracted_video_urls.extend(extracted_video_urls_inner)
            print(f"For company {site.name} the note urls are "
                  f"{len(extracted_nota_urls)} and video are {len(extracted_video_urls_inner)}")
 
            # Process Note Urls
            note_metrics = process_urls(extracted_nota_urls, PERFORMANCE_METRICS.copy(), site, job_type="GENERAL JOB")
            
            # Process video URLs
            video_metrics = process_urls(extracted_video_urls, PERFORMANCE_METRICS.copy(), site, url_type="video", job_type="GENERAL JOB")
            
            print(f"SCORE IS {site.name} NOTE: {note_metrics} VIDEO: {video_metrics}")
            
            record = create_or_update_record(
                model_class=Record, 
                note_metrics=note_metrics,
                video_metrics=video_metrics,
                site=site,
                date=date,
            )
            
            write_text_to_file(f"Generel Record IS {record.name} NOTE: {record.note_value} VIDEO: {record.video_value}", OTHER_RECORD_FILEPATH)
            return record
        except Exception as e:
            # Log the exception with a more detailed message
            print(f"Exception occurred while processing site '{site.name}' on {date}: {e}")
            
            # Attempt to create the record if not already exists
            record, created = create_record_if_not_exists(
                model_class=Record,
                site=site,
                date=date,
            )
            
            # Log the outcome of the create operation after an exception
            if created:
                write_text_to_file(
                    f"Exception occurred: New General Record created for site '{record.name}' with NOTE: {record.note_value} and VIDEO: {record.video_value} due to an error.",
                    OTHER_RECORD_FILEPATH
                )
            else:
                write_text_to_file(
                    f"Exception occurred: Existing General Record found for site '{record.name}' with NOTE: {record.note_value} and VIDEO: {record.video_value}. No changes were made due to an error.",
                    OTHER_RECORD_FILEPATH
                )
                
            return record

def run_job():

    sites = Site.objects.all()
    semaphore = threading.Semaphore(4)
    print(f"SITES ARE {sites}")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_site = {executor.submit(
            process_site, site, semaphore): site for site in sites}
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            result = future.result()  # Get the result of the future
            print(f"Processed site {site}: Result = {result}")
    print(f"STATUS IS DONE")

class Command(BaseCommand):
    help = 'Run a long function in a separate thread'

    def handle(self, *args, **kwargs):
        print(f"SSTARTING")
        run_job()
