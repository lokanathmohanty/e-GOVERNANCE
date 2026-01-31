from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('services-list/', views.services_list, name='services_list'),
    path('dashboard-info/', views.dashboard_info_view, name='dashboard_info'),
    path('help/', views.help_page, name='help'),
    path('manuals/', views.manuals, name='manuals'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('accessibility/', views.accessibility, name='accessibility'),

    path('', views.home, name='home'),
    path('contact/', views.contact_us, name='contact'),
    path('notifications/', views.all_notifications, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_notification_read, name='mark_read'),
    path('notifications/read/all/', views.mark_all_read, name='mark_all_read'),
    path('verify-certificate/', views.verify_public_certificate, name='verify_certificate'),
    path('healthz', views.health_check, name='health_check'),
]
