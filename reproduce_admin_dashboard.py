
import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from admin_panel.views import dashboard
from core.models import SystemConfiguration

def reproduce():
    # Ensure config exists
    try:
        SystemConfiguration.objects.get_or_create(id=1)
    except Exception as e:
        print(f"Warning creating config: {e}")

    # Create admin user if not exists
    try:
        user, created = User.objects.get_or_create(username='admin_test', email='admin@test.com', defaults={'role': 'admin'})
        if created:
            user.set_password('password')
            user.save()
            print("Admin user created")
    except Exception as e:
        print(f"User creation/fetch error: {e}")
        return

    factory = RequestFactory()
    request = factory.get('/admin-panel/dashboard/')
    request.user = user
    
    # Add messages support
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    try:
        response = dashboard(request)
        print(f"Response Code: {response.status_code}")
        if response.status_code == 200:
            print("Dashboard loaded successfully")
        else:
            print(f"Dashboard failed with code: {response.status_code}")
            
        # If it's a template response, we might need to render it to trigger the error
        if hasattr(response, 'render'):
            response.render()
            print("Template rendered successfully")
            
    except Exception as e:
        print("Exception caught during dashboard execution:")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reproduce()
