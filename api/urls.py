from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('services/', views.service_list_api, name='service_list'),
    path('status/<str:app_no>/', views.application_status_api, name='app_status'),
    path('dept-stats/', views.department_stats_api, name='dept_stats'),
]
