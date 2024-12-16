import subprocess
import random
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import re
import concurrent.futures
import json
import os
import threading

from server.constants import AMP_PARAMS, FACTOR, OTHER_RECORD_FILEPATH
from server.models import ErrorLog

def write_text_to_file(text, filename=OTHER_RECORD_FILEPATH):
    # Open the file in append mode; create it if it doesn't exist
    with open(filename, "a") as file:
        # Write the text with a newline at the end
        file.write(text + "\n")
        
def sanitize_filename(url):
    """Sanitize the URL to create a safe filename."""
    return re.sub(r'[\/:*?"<>|]', '_', url)
        
def get_lighthouse_mobile_score(url, job_type, log_file_name=OTHER_RECORD_FILEPATH):
    """
    Fetch Lighthouse performance metrics for a given URL.
    Divides time-based metrics by 1000 to convert from ms to s.
    """
    performance_score = 0
    first_contentful_paint = 0
    total_blocking_time = 0
    speed_index = 0
    largest_contentful_paint = 0
    cumulative_layout_shift = 0
    report_file_path_rel = sanitize_filename(f"report_{url}.json")
    report_file_path = f'{os.getcwd()}/{report_file_path_rel}'

    try:
        # Run Lighthouse and generate a JSON report
        # command = f'lighthouse --no-enable-error-reporting --chrome-flags="--headless" --output=json --output-path="{report_file_path_rel}" "{url}"'
        command = (
            f'lighthouse --no-enable-error-reporting '
            f'--chrome-flags="--headless --disable-gpu --no-sandbox" '
            f'--throttling-method=provided '
            f'--output=json --output-path="{report_file_path_rel}" "{url}"'
        )
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        code = result.check_returncode()

        if code != 0:
            write_text_to_file(f"FOR URL {url} ERROR IS {result.stdout.decode('utf-8')}"), log_file_name
            print(result.stdout.decode('utf-8'))

        # Parse the Lighthouse report
        with open(report_file_path, 'r', encoding='utf-8') as file:
            report = json.load(file)
            if report['categories']['performance']['score'] is not None:
                performance_score = report['categories']['performance']['score'] * FACTOR
                print(f"raw scoor for job: {job_type} url: {url}: ", performance_score)
                if(performance_score == 0):
                    write_text_to_file(f"FOR URL {url} SCORE IS 0", filename=OTHER_RECORD_FILEPATH)
                if performance_score >= 100:
                    performance_score = 100

            audits = report.get('audits', {})
            # Divide time-based metrics by 1000 to convert from ms to s
            first_contentful_paint = audits.get('first-contentful-paint', {}).get('numericValue', 0) / 1000
            total_blocking_time = audits.get('total-blocking-time', {}).get('numericValue', 0) / 1000
            speed_index = audits.get('speed-index', {}).get('numericValue', 0) / 1000
            largest_contentful_paint = audits.get('largest-contentful-paint', {}).get('numericValue', 0) / 1000
            cumulative_layout_shift = audits.get('cumulative-layout-shift', {}).get('numericValue', 0)

            write_text_to_file(f"METRICS FOR URL {url}: "
                               f"Performance Score: {performance_score}, "
                               f"First Contentful Paint: {first_contentful_paint} s, "
                               f"Total Blocking Time: {total_blocking_time} s, "
                               f"Speed Index: {speed_index} s, "
                               f"Largest Contentful Paint: {largest_contentful_paint} s, "
                               f"Cumulative Layout Shift: {cumulative_layout_shift}", log_file_name)

    except subprocess.CalledProcessError as e:
        write_text_to_file(f"FOR URL {url} ERROR: {e.stderr.decode('utf-8')}", log_file_name)
        print(f"Error running Lighthouse for {url}: {e.stderr.decode('utf-8')}")
    except Exception as e:
        write_text_to_file(f"FOR URL {url} GENERAL ERROR: {e}", log_file_name)
        print(f"General error processing {url}: {e}")
    finally:
        # Clean up the report file
        if os.path.exists(report_file_path):
            os.remove(report_file_path)

    return {
        "performance_score": performance_score,
        "first_contentful_paint": first_contentful_paint,
        "total_blocking_time": total_blocking_time,
        "speed_index": speed_index,
        "largest_contentful_paint": largest_contentful_paint,
        "cumulative_layout_shift": cumulative_layout_shift
    }
    
def process_urls(extracted_urls, metrics, site, url_type="note", job_type="Not specify", log_file_name=OTHER_RECORD_FILEPATH, **kwargs):
    is_amp = kwargs.get("is_amp", False)
    total_values_count = 0
    successful_site_performance = 0
    for url in extracted_urls:
        if is_amp:
            url = f"{url}{AMP_PARAMS}"

        if successful_site_performance >= 10:
            break
        try:
            res = get_lighthouse_mobile_score(url, job_type, log_file_name=log_file_name)
            print(f"{job_type} Metrics for {url_type} URL {url} for site {site.name}: {res}")
            if res["performance_score"] != 0:
                successful_site_performance +=1
                for key in metrics:
                    metrics[key] += res[key]
                total_values_count += 1
        except Exception as e:
            log = ErrorLog(message=f"Failed for {url_type} URL {url}: {e}")
            log.save()
            
    # Calculate averages
    for key in metrics:
        metrics[key] = metrics[key] / (total_values_count or 1)      

    # Multiply performance scores by 100 to convert to percentage
    metrics["performance_score"] *= 100
    
    return metrics

def create_or_update_record(model_class, note_metrics, video_metrics, site, date):
    """
    Creates a record based on the provided metrics and model class.
    """
    try:
        # Calculate total value (example: average of note and video performance scores)
        total_value = (note_metrics["performance_score"] + video_metrics["performance_score"]) / 2
        
        # Create the record using the provided model class
        record, created = model_class.objects.update_or_create(
            name=site.name, 
            date=date,
            defaults={
                'note_value': note_metrics.get("performance_score", 0),
                'video_value': video_metrics.get("performance_score", 0),
                'azteca': "Azteca" in site.name,
                'total_value': total_value,
                # Additional note metrics
                'note_first_contentful_paint': note_metrics.get("first_contentful_paint", 0),
                'note_total_blocking_time': note_metrics.get("total_blocking_time", 0),
                'note_speed_index': note_metrics.get("speed_index", 0),
                'note_largest_contentful_paint': note_metrics.get("largest_contentful_paint", 0),
                'note_cumulative_layout_shift': note_metrics.get("cumulative_layout_shift", 0),
                # Additional video metrics
                'video_first_contentful_paint': video_metrics.get("first_contentful_paint", 0),
                'video_total_blocking_time': video_metrics.get("total_blocking_time", 0),
                'video_speed_index': video_metrics.get("speed_index", 0),
                'video_largest_contentful_paint': video_metrics.get("largest_contentful_paint", 0),
                'video_cumulative_layout_shift': video_metrics.get("cumulative_layout_shift", 0),
            }
        )

        return record
    
    except Exception as e:
        # print(f"Error creating record for site {site.name}: {e}")
        # Optionally log the error to a database or a file
        log = ErrorLog(message=f"Error creating record for {site.name}: {e}")
        log.save()
        return None

def create_record_if_not_exists(model_class, site, date):
    """
    Creates a record with default values for the given model if it doesn't already exist.
    """
    try:
        # Attempt to get an existing record. If it doesn't exist, create a new one.
        record, created = model_class.objects.get_or_create(
            name=site.name, 
            date=date,
            defaults={
                'note_value': 0,
                'video_value': 0,
                'azteca': "Azteca" in site.name,
                'total_value': 0,
            }
        )

        return record, created
    
    except Exception as e:
        # print(f"Error creating default record for site {site.name}: {e}")
        # Optionally log the error to a database or a file
        log = ErrorLog(message=f"Error creating default record for {site.name}: {e}")
        log.save()
        return None

def get_weeks_in_past_six_months():
    # Get today's date
    today = datetime.today()

    # Find the most recent Monday
    days_since_monday = today.weekday()  # Monday is 0, Sunday is 6
    start_of_week = today - timedelta(days=days_since_monday)

    # Calculate the date 6 months ago
    six_months_ago = today - timedelta(weeks=4 * 6)  # Approximation of 6 months

    # List to store the weeks
    weeks = []

    # Loop backwards and collect the Mondays
    current_week = start_of_week
    while current_week >= six_months_ago:
        weeks.append(current_week.date())
        current_week -= timedelta(weeks=1)

    return weeks

def get_previous_months_of_current_year():
    current_year = datetime.now().year

    # Get the current month
    current_month = datetime.now().month

    # Generate a list of previous months (excluding the current month)
    previous_months = [f"{current_year}-{month:02d}" for month in range(1, current_month)]
    
    return previous_months

def create_empty_records(sites, model_class):
    today = datetime.today()
    monday_of_current_week = today - timedelta(days=today.weekday())
    date = monday_of_current_week.date()
    
    records_to_create = []

    for site in sites:
        if model_class.objects.filter(name=site.name, date=date).exists():
            print(site.name, 'exists')
            continue

        record = model_class(
            name=site.name,
            note_value=0.0,
            video_value=0.0,
            total_value=0.0,
            azteca="Azteca" in site.name,
            date=date
        )
        records_to_create.append(record)

    model_class.objects.bulk_create(records_to_create)
