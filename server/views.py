from django.shortcuts import render
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
    data = get_insights()
    return JsonResponse(data, safe=False)
