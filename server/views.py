from django.shortcuts import render
from django.http import JsonResponse
from .get_data import get_data
# Create your views here.


def handle_request(request):
    data = get_data()
    return JsonResponse(data, safe=False)
