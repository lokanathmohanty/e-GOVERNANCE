from django.urls import path
from . import views

app_name = 'mis'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inbox/', views.contact_inbox, name='contact_inbox'),
    path('reply/<int:msg_id>/', views.reply_contact, name='reply_contact'),
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_create, name='service_create'),
    path('services/edit/<int:service_id>/', views.service_edit, name='service_edit'),
    path('reports/export/', views.export_reports, name='export_reports'),
]
