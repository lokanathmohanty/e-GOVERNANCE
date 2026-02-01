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

from django.urls import re_path
from django.views.static import serve

# Serve media files in development AND production (for Render disk storage compatibility)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
