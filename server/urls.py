from django.urls import path

from server.amp_data.amp_apis import AmpPerformanceReportView
from . import views

urlpatterns = [
    path('', views.handle_request, name='handle_request'),
    path('quarter', views.get_quarterly, name='quarter'),
    path('insights', views.get_insights_api, name='insights'),
    path('local', views.get_local_data, name='local'),
    path('local/quarter', views.get_local_quarterly, name='local-quarter'),
    path('local/insights', views.get_local_insights_api, name='local-insights'),
    path('amp', views.get_amp_data, name='amp'),
    path('amp/quarter', views.get_amp_quarterly, name='amp-quarter'),
    path('amp/insights', views.get_amp_insights_api, name='amp-insights'),
    path('amp/performance', AmpPerformanceReportView.as_view(), name='amp-performance'),

    # path('run_job', views.run_job, name='run_job'),
]
