from django.urls import path

from server.amp_data.amp_apis import AmpPerformanceReportView
from server.get_data import GeneralPerformanceReportView
from server.local_data.local_insights import LocalPerformanceReportView
from . import views

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

    # path('run_job', views.run_job, name='run_job'),
]
