from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle_request, name='handle_request'),
    path('quarter', views.get_quarterly, name='quarter'),
    path('insights', views.get_quarterly, name='quarter'),
]
