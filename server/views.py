from django.shortcuts import render
import threading
from django.core.management import call_command
import os
import subprocess
import json
from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
from .models import Record, Site, ErrorLog
from .generate_reports import fetch_data, get_latest_urls, get_sorted_rss_items
# Create your views here.


def handle_request(_request):
    data = get_data()
    return JsonResponse(data, safe=False)


def get_quarterly(_request):
    data = get_averages()
    return JsonResponse(data, safe=False)


def get_insights_api(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    print(f"FILT {start} {end}")
    data = get_insights({
        "start": start,
        "end": end
    })
    return JsonResponse(data, safe=False)


def run_job(_request):
    threading.Thread(target=run_proj).start()
    return JsonResponse({
        "status": "success"}, safe=False)


def run_proj():
    call_command("run_job")

# run_job(None)

# url= 'https://www.nytimes.com/sitemaps/new/news.xml.gz'
# data = fetch_data(url)
# print(get_latest_urls(data))
