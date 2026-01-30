from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),              # Landing page
    path('accounts/', include('accounts.urls')),  # Auth
    path('citizen/', include('citizen.urls')),    # Citizen module
    path('officer/', include('officer.urls')),    # Officer module
    path('mis/', include('mis.urls')),            # MIS Dashboard
    path('admin-panel/', include('admin_panel.urls')),  # Admin
    path('api/', include('api.urls')),            # REST APIs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
