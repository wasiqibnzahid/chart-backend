import subprocess
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import concurrent.futures
import json
import os
import threading
from ...models import ErrorLog, Record, Site
from ...generate_reports import fetch_data, fetch_feed_urls, get_latest_urls, get_sorted_rss_items


def process_site(site: Site, semaphore):
    with semaphore:
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
                log = ErrorLog(message=f"Sitemap returned 0 urls: {note_sitemap_url}")
                log.save()
            if len(extracted_video_urls_inner) == 0:
                log = ErrorLog(message=f"Sitemap returned 0 urls: {video_sitemap_url}")
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
            while index < 1 and i < len(extracted_nota_urls):
                try:
                    res = get_lighthouse_mobile_score(
                        extracted_nota_urls[i])
                    print(f"FOR nota URL {extracted_nota_urls[i]} FOR SITE {site.name} score is {res}")
                    if res != 0:
                        note_val += res
                        note_count += 1
                        index += 1
                except:
                    url = extracted_nota_urls[i]
                    log = ErrorLog(
                        message=f"Failed for Manual Url {url}"
                    )
                    log.save()
                i += 1

            i = 0
            index = 0
            while index < 1 and i < len(extracted_video_urls):
                try:
                    res = get_lighthouse_mobile_score(
                        extracted_video_urls[i])
                    print(f"FOR video URL {extracted_nota_urls[i]} FOR SITE {site.name} score is {res}")
                    if res != 0:
                        video_val += res
                        video_count += 1
                        index += 1
                except:
                    url = extracted_video_urls[i]
                    log = ErrorLog(
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
            record = Record(
                name=site.name,
                note_value=note_val,
                video_value=video_val,
                azteca=site.name == "Azteca",
                date=date,
                total_value=(note_val + video_val) / 2
                # Set Azteca flag if applicable
            )
            return record

        except Exception as e:
            print(f"Exception for {site.name}: {e}")
            return Record(name=site.name,
                          note_value=0,
                          video_value=0,
                          azteca="Azteca" in site.name,
                          date=date,
                          total_value=0
                          )


def run_job():
    sites = Site.objects.all()
    records = []
    semaphore = threading.Semaphore(3)

    with concurrent.futures.ThreadPoolExecutor() as executor:

        future_to_site = {executor.submit(
            process_site, site, semaphore): site for site in sites}
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            result = future.result()  # Get the result of the future
            records.append(result)
            print(f"Processed site {site}: Result = {result}")

    if records:
        Record.objects.bulk_create(records)


def sanitize_filename(url):
    # Replace invalid characters with underscores
    safe_url = re.sub(r'[\/:*?"<>|]', '_', url)
    return safe_url


def get_lighthouse_mobile_score(url):
    performance_score = 0
    report_file_path_rel = sanitize_filename(f"report_{url}.json")
    report_file_path = f'{os.getcwd()}/{report_file_path_rel}'
    try:
        command = f'lighthouse --no-enable-error-reporting --chrome-flags="--headless --disable-gpu" --output=json --output-path="{report_file_path_rel}" "{url}"'
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        code = result.check_returncode()
        if code != 0:
            print(result.stdout)

        # pipe = os.popen(
        #     f'lighthouse --chrome-flags="--headless" --output=json --output-path="{report_file_path_rel}" ' + url)
        # pipe.read()

        with open(report_file_path, 'r', encoding='utf-8') as file:
            report = json.load(file)
            if report['categories']['performance']['score']:
                performance_score = report['categories']['performance']['score']
    except Exception as e:
        print(f"Error {e}")
    finally:
        if os.path.exists(report_file_path):
            os.remove(report_file_path)
    return performance_score


class Command(BaseCommand):
    help = 'Run a long function in a separate thread'

    def handle(self, *args, **kwargs):
        run_job()
        # threading.Thread(target=run_job, daemon=True).start()
        # self.stdout.write(self.style.SUCCESS(
        #     'Started long function in background.'))
