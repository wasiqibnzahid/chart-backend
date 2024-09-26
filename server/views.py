from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
from .models import ErrorLog
from server.local_data import local_data,local_quarter,local_insights
# Create your views here.


def handle_request(_request):
    data = get_data()
    errors = ErrorLog.objects.all().order_by("-created_at")[:5]
    formatted_errors = [{"id": error.id, "message": error.message,
                         "created_at": error.created_at.isoformat()} for error in errors]

    # Add errors to the data dictionary
    data["errors"] = formatted_errors
    data["errors"] = data['errors'] + data["errors"]
    data["errors"] = data['errors'] + data["errors"]
    return JsonResponse(data, safe=False)


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
    errors = ErrorLog.objects.all().order_by("-created_at")[:5]
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
    start = request.GET.get("start")

    end = request.GET.get("end")
    if not start:
        start = "01-2024"
    if not end:
        end = "12-2024"

    data = local_insights.get_insights({
        "start": start,
        "end": end
    })
    return JsonResponse(data, safe=False)

# def run_job(_request):
#     threading.Thread(target=run_proj, daemon=True).start()
#     return JsonResponse({
#         "status": "success"}, safe=False)


# def run_proj():
#     call_command("run_job")

# run_job(None)

# url= 'https://www.nytimes.com/sitemaps/new/news.xml.gz'
# data = fetch_data(url)
# print(get_latest_urls(data))
