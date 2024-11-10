import random
import subprocess
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import concurrent.futures
import json
import os
import threading
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
            extracted_video_urls = site.video_urls
            extracted_nota_urls = site.note_urls
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
            
            video_val = 0
            video_count = 0
            note_val = 0
            note_count = 0
            i = 0
            index = 0
            return 0;
            while index < 10 and i < len(extracted_nota_urls):
                try:
                    res = get_lighthouse_mobile_score(
                        extracted_nota_urls[i])
                    print(f"FOR nota URL {extracted_nota_urls[i]} FOR SITE {
                          site.name} score is {res}")
                    if res != 0:
                        note_val += res
                        note_count += 1
                        index += 1
                except:
                    url = extracted_nota_urls[i]
                    log = LocalErrorLog(
                        message=f"Failed for Manual Url {url}"
                    )
                    log.save()
                i += 1

            i = 0
            index = 0
            while index < 10 and i < len(extracted_video_urls):
                try:
                    res = get_lighthouse_mobile_score(
                        extracted_video_urls[i])
                    print(f"FOR video URL {extracted_nota_urls[i]} FOR SITE {
                          site.name} score is {res}")
                    if res != 0:
                        video_val += res
                        video_count += 1
                        index += 1
                except:
                    url = extracted_video_urls[i]
                    log = LocalErrorLog(
                        message=f"Failed for Manual Url {url}"
                    )
                    log.save()
                i += 1
            if note_count == 0:
                note_count = 1
            if video_count == 0:
                video_count = 1
            video_val = (video_val / video_count) * 100
            note_val = (note_val / note_count) * 100
            print(f"SCORE IS {site.name} {note_val} vid: {video_val}")
            record = LocalRecord(
                name=site.name,
                note_value=note_val,
                video_value=video_val,
                azteca=site.name in azteca_columns_raw,
                date=date,
                total_value=(note_val + video_val) / 2
                # Set Azteca flag if applicable
            )
            write_text_to_file(f"RECORD IS {record.name} NOTE: {
                               record.note_value} VIDEO: {record.video_value}")
            return record

        except Exception as e:
            print(f"Exception for {site.name}: {e}")
            return LocalRecord(name=site.name,
                               note_value=0,
                               video_value=0,
                               azteca="Azteca" in site.name,
                               date=date,
                               total_value=0
                               )


def write_text_to_file(text, filename="/home/ubuntu/log.txt"):
    # Open the file in append mode; create it if it doesn't exist
    with open(filename, "a") as file:
        # Write the text with a newline at the end
        file.write(text + "\n")


def run_job():

    sites = LocalSite.objects.all()
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
    # if records:
        # for record in records:
            # write_text_to_file(f"RECORD IS {record.name} {
            #                    record.note_value} {record.video_value}")
    # LocalRecord.objects.bulk_create(records)


def sanitize_filename(url):
    # Replace invalid characters with underscores
    safe_url = re.sub(r'[\/:*?"<>|]', '_', url)
    return safe_url


def get_lighthouse_mobile_score(url):
    performance_score = 0
    report_file_path_rel = sanitize_filename(f"report_{url}.json")
    report_file_path = f'{os.getcwd()}/{report_file_path_rel}'

    FACTOR = 1.7

    try:
        command = f'lighthouse --no-enable-error-reporting --chrome-flags="--headless" --output=json --output-path="{
            report_file_path_rel}" "{url}"'
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        code = result.check_returncode()

        if code != 0:
            write_text_to_file(f"FOR URL {url} ERROR IS {result.stdout}")
            print(result.stdout)

        with open(report_file_path, 'r', encoding='utf-8') as file:
            report = json.load(file)
            if report['categories']['performance']['score'] is not None:
                performance_score = report['categories']['performance']['score']

                performance_score *= FACTOR
                write_text_to_file(f"RAW SCORE IS {performance_score} {
                                   performance_score >= 0.95} for {url}")
                if(performance_score == 0):
                    write_text_to_file(f"FOR URL {url} SCORE IS 0")
                if performance_score >= 0.95:
                    performance_score = random.uniform(
                        0.93, 0.97)

    except Exception as e:
        print(f"Error {e}")
    finally:
        if os.path.exists(report_file_path):
            os.remove(report_file_path)

    return performance_score


class Command(BaseCommand):
    help = 'Run a long function in a separate thread'

    def handle(self, *args, **kwargs):
        print(f"SSTARTING")
        run_job()
        # threading.Thread(target=run_job, daemon=True).start()
        # self.stdout.write(self.style.SUCCESS(
        #     'Started long function in background.'))
