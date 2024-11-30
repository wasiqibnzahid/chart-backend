from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
from .models import LocalErrorLog
from server.local_data import local_data,local_quarter,local_insights
from server.amp_data import amp_data
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
