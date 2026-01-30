from django.urls import path
from . import views

app_name = 'citizen'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('services/', views.services_list, name='services'),
    path('apply/<int:service_id>/', views.apply_service, name='apply'),
    path('application/<int:app_id>/', views.application_detail, name='detail'),
    path('application/<int:app_id>/receipt/', views.application_receipt, name='receipt'),
    path('track/', views.public_track, name='public_track'),
    path('application/<int:app_id>/certificate/', views.download_certificate, name='certificate'),
    path('grievances/', views.grievances, name='grievances'),
    path('locker/', views.document_locker, name='locker'),
    path('id-card/', views.digital_id_card, name='id_card'),
    path('appointments/', views.my_appointments, name='appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('family/', views.family_members, name='family'),
    path('security/', views.security_dashboard, name='security'),
    path('poll/vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
    path('feedback/<int:app_id>/', views.submit_feedback, name='submit_feedback'),
]
