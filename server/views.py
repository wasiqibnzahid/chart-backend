from django.shortcuts import render
import json
from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
# Create your views here.


def handle_request(_request):
    data = get_data()
    return JsonResponse(data, safe=False)


def get_quarterly(_request):
    data = get_averages()
    return JsonResponse(data, safe=False)


def get_insights_api(_request):
    start = _request.GET.get("start")
    end = _request.GET.get("end")
    print(f"FILT {start} {end}")
    data = get_insights({
        "start": start,
        "end": end
    })
    return JsonResponse(data, safe=False)
