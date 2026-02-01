import os
import django
from django.template import loader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Application
User = get_user_model()

templates = [
    ('accounts/profile.html', {'user': User.objects.first() or User(username='testuser', role='citizen'), 'form': {}}),
    ('citizen/track.html', {'user': User.objects.first() or User(username='testuser', role='citizen'), 'app': Application.objects.first()}),
    ('citizen/dashboard_bootstrap.html', {'user': User.objects.first(), 'applications': [], 'approved_apps': [], 'stats': {}}),
]

for name, ctx in templates:
    try:
        t = loader.get_template(name)
        t.render(ctx)
        print(f"SUCCESS: {name}")
    except Exception as e:
        print(f"FAILURE: {name} - {e}")
