from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/', views.manage_departments, name='departments'),
    path('services/', views.manage_services, name='services'),
    path('audit-logs/', views.view_audit_logs, name='audit_logs'),
    path('users/', views.manage_users, name='users'),
    path('announcements/', views.manage_announcements, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
]
