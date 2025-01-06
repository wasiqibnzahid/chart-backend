from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
from .models import LocalErrorLog, WebsiteCheck
from server.local_data import local_data,local_quarter,local_insights
from server.amp_data import amp_data
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from django.conf import settings

# Add constant for Lambda URL
LAMBDA_URL = "https://hpuyeonhb3mctgalziaie3py7m0vnqfk.lambda-url.us-east-1.on.aws/"

# Create your views here.


def handle_request(_request):
    try:
        data = get_data()
        if not data:
            raise ValueError("No data available")
            
        errors = LocalErrorLog.objects.all().order_by("-created_at")[:5]
        formatted_errors = [{
            "id": error.id,
            "message": error.message,
            "created_at": error.created_at.isoformat()
        } for error in errors]
        
        data["errors"] = formatted_errors
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "details": "Failed to handle request",
            "status": "error"
        }, status=500)


def get_quarterly(_request):
    data = get_averages()
    return JsonResponse(data, safe=False)


def get_insights_api(request):
    start = request.GET.get("start")

    end = request.GET.get("end")
    if not start:
        start = "01-2024"
    if not end:
        end = "12-2024"
    data = get_insights({
        "start": start,
        "end": end
    })
    return JsonResponse(data, safe=False)


def get_local_data(request):
    data = local_data.get_data()
    errors = LocalErrorLog.objects.all().order_by("-created_at")[:5]
    formatted_errors = [{"id": error.id, "message": error.message,
                         "created_at": error.created_at.isoformat()} for error in errors]

    # Add errors to the data dictionary
    data["errors"] = formatted_errors
    data["errors"] = data['errors'] + data["errors"]
    data["errors"] = data['errors'] + data["errors"]
    return JsonResponse(data, safe=False)

def get_local_quarterly(_request):
    data = local_quarter.get_averages()
    return JsonResponse(data, safe=False)

def get_local_insights_api(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        data = local_insights.get_insights({
            'start': start,
            'end': end
        })
        if isinstance(data, dict) and 'error' in data:
            return JsonResponse(data, status=500)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'details': 'Failed to get insights'
        }, status=500)

def get_amp_data(request):
    try:
        data = amp_data.get_data()
        errors = LocalErrorLog.objects.all().order_by("-created_at")[:5]
        formatted_errors = [{"id": error.id, "message": error.message,
                           "created_at": error.created_at.isoformat()} for error in errors]
        
        # Add errors to the data dictionary (only once)
        data["errors"] = formatted_errors
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({
            "error": str(e)
        }, status=500)

def get_amp_quarterly(_request):
    data = amp_data.get_averages()
    return JsonResponse(data, safe=False)

def get_amp_insights_api(request):
    start = request.GET.get("start")

    end = request.GET.get("end")
    if not start:
        start = "01-2024"
    if not end:
        end = "12-2024"

    data = amp_data.get_insights({
        "start": start,
        "end": end
    })
    return JsonResponse(data, safe=False)

def add_website_check(request):
    try:
        url = request.GET.get('url')
        
        if not url:
            return JsonResponse({
                'error': 'URL is required'
            }, status=400)
        
        website_check = WebsiteCheck.objects.filter(url=url, status='waiting').first()
        if not website_check:
            website_check = WebsiteCheck.objects.create(
                url=url,
                status='waiting'
            )
        
        # Notify Lambda about new check
        try:
            response = requests.get(LAMBDA_URL)
            print(f"Lambda notification response for new check: {response.text}")
        except Exception as e:
            print(f"Error notifying Lambda about new check: {e}")
        
        return JsonResponse({
            'id': website_check.id,
            'url': website_check.url,
            'status': website_check.status,
            'created_at': website_check.created_at.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def list_website_checks(request):
    try:
        site = request.GET.get('site')
        checks = [];
        if site:
            checks = WebsiteCheck.objects.filter(url=site)
            
        return JsonResponse({
            'checks': [{
                'id': check.id,
                'url': check.url,
                'status': check.status,
                'json': check.json_data,
                'created_at': check.created_at.isoformat(),
                'updated_at': check.updated_at.isoformat(),
                'metrics': check.metrics
            } for check in checks]
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

