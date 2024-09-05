import threading
from django.core.management import call_command
from django.http import JsonResponse
from .get_data import get_data, get_averages, get_insights
from .models import ErrorLog
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
    print(f"FILT {start} {end}")
    data = get_insights({
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
