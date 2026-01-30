from django.urls import path
from . import views

app_name = 'officer'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/<int:app_id>/', views.review_application, name='review'),
]
