from django.core.management.base import BaseCommand
import json
import os
import threading
from ...models import ErrorLog, Record, Site
from ...generate_reports import fetch_data, fetch_feed_urls, get_latest_urls, get_sorted_rss_items


def run_job():
    sites = Site.objects.all()
    records = []
    for site in sites:
        try:
            note_sitemap_url = site.sitemap_url
            video_sitemap_url = site.sitemap_url
            if (site.note_sitemap_url):
                note_sitemap_url = site.note_sitemap_url
            if (site.video_sitemap_url):
                video_sitemap_url = site.video_sitemap_url
            nota_xml = fetch_data(note_sitemap_url)
            video_xml = fetch_data(video_sitemap_url)
            extracted_video_urls = site.video_urls
            extracted_nota_urls = site.note_urls
            if (site.name == 'El Heraldo'):
                extracted_video_urls_inner, extracted_nota_urls_inner = get_latest_urls(
                    site.sitemap_url, is_xml=False)
            elif (site.name == "AS"):
                extracted_nota_urls_inner = get_sorted_rss_items(
                    site.note_sitemap_url)
                extracted_video_urls_inner = get_sorted_rss_items(
                    site.video_sitemap_url)
            else:
                extracted_nota_urls_inner = get_latest_urls(
                    nota_xml, is_xml="html" not in note_sitemap_url)
                extracted_video_urls_inner = get_latest_urls(
                    video_xml, is_xml="html" not in video_sitemap_url)
            if (site.name == "Milenio" or site.name == "El Universal"):
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "video" not in item]
                extracted_video_urls_inner = [
                    item for item in extracted_video_urls_inner if "video" in item]
            if (site.name == "Infobae" or site.name == "AS"):
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "video" not in item]
            if (site.name == "Terra"):
                extracted_nota_urls_inner = [
                    item for item in extracted_nota_urls_inner if "nacionales" in item]
                extracted_video_urls_inner = [
                    item for item in extracted_video_urls_inner if "entretenimiento" in item]
            if len(extracted_nota_urls_inner) == 0:
                log = ErrorLog(message=f"Sitemap returned 0 urls: {
                               note_sitemap_url}")
                log.save()
            if len(extracted_video_urls_inner) == 0:
                log = ErrorLog(message=f"Sitemap returned 0 urls: {
                               video_sitemap_url}")
                log.save()

            extracted_nota_urls.extend(extracted_nota_urls_inner)
            extracted_video_urls.extend(extracted_video_urls_inner)
            print(f"For company {site.name} the note urls are {
                len(extracted_nota_urls)} and video are {len(extracted_video_urls_inner)}")
            video_val = 0
            video_count = 0
            note_val = 0
            note_count = 0
            i = 0
            while (i < 10 and i < len(extracted_nota_urls)):
                try:
                    note_val += get_lighthouse_mobile_score(
                        extracted_nota_urls[i])
                    note_count += 1
                except:
                    url = extracted_nota_urls[i]
                    log = ErrorLog(
                        message=f"Failed for Manual Url {url}"
                    )
                    log.save()
                i += 1

            i = 0
            while (i < 10 and i < len(extracted_video_urls)):
                try:
                    video_val += get_lighthouse_mobile_score(
                        extracted_video_urls[i])
                    video_count += 1
                except:
                    url = extracted_video_urls[i]
                    log = ErrorLog(
                        message=f"Failed for Manual Url {url}"
                    )
                    log.save()
                i += 1
            if (note_count == 0):
                note_count = 1
            if (video_count == 0):
                video_count = 1
            video_val = ((video_val)/video_count) * 100
            note_val = ((note_val)/note_count) * 100
            record = Record(
                name=site.name,
                note_value=note_val,
                video_value=video_val,
                azteca=site.name == "Azteca"  # Set Azteca flag if applicable
            )
            records.append(record)

        except Exception as e:
            print(f"Exception for {site.name}: {e}")
    if records:
        Record.objects.bulk_create(records)


def get_lighthouse_mobile_score(url):
    pipe = os.popen(
        'lighthouse --chrome-flags="--headless" --output=json --output-path=report_3.json ' + url)
    pipe.read()
    with open('C:/py work/report_3.json', 'r', encoding='utf-8') as file:
        report = json.load(file)

    performance_score = report['categories']['performance']['score']
    return performance_score


def ab():
    print("WOW AB")


class Command(BaseCommand):
    help = 'Run a long function in a separate thread'

    def handle(self, *args, **kwargs):
        threading.Thread(target=run_job, daemon=True).start()
        self.stdout.write(self.style.SUCCESS(
            'Started long function in background.'))
