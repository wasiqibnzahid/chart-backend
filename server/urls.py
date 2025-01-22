from django.urls import path
from django.http import JsonResponse

from server.amp_data.amp_apis import AmpPerformanceReportView
from server.get_data import GeneralPerformanceReportView
from server.local_data.local_insights import LocalPerformanceReportView
from . import views
from . import image_data

urlpatterns = [
    path('', views.handle_request, name='handle_request'),
    path('quarter/', views.get_quarterly, name='quarter'),
    path('insights/', views.get_insights_api, name='insights'),
    path('performance/', GeneralPerformanceReportView.as_view(), name='general-performance'),
    path('local/', views.get_local_data, name='local'),
    path('local/quarter/', views.get_local_quarterly, name='local-quarter'),
    path('local/insights/', views.get_local_insights_api, name='local-insights'),
    path('local/performance/', LocalPerformanceReportView.as_view(), name='local-performance'),
    path('amp/', views.get_amp_data, name='amp'),
    path('amp/quarter/', views.get_amp_quarterly, name='amp-quarter'),
    path('amp/insights/', views.get_amp_insights_api, name='amp-insights'),
    path('amp/performance/', AmpPerformanceReportView.as_view(), name='amp-performance'),
    path('api/website-checks/', views.list_website_checks, name='list_website_checks'),
    path('api/website-checks/add/', views.add_website_check, name='add_website_check'),
    path('image-data/', views.handle_image_request, name='handle_image_request'),
    path('image-data/quarter/', lambda request: JsonResponse(image_data.get_image_averages()), name='image_quarter'),
    path('image-data/insights/', lambda request: JsonResponse(image_data.get_image_insights({
        'start': request.GET.get('start', '01-2024'),
        'end': request.GET.get('end', '12-2024')
    })), name='image_insights'),
    path('image-data/records/', image_data.GetImageRecordsView.as_view(), name='image_records'),

    # path('run_job', views.run_job, name='run_job'),
]
