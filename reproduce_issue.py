import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from citizen import views
from core.models import User, Service, Department

def run():
    print("Starting reproduction script...")
    
    # 1. Setup User
    username = 'repro_user_citizen'
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password='password', role='citizen')
        print(f"Created user {username}")
    
    # 2. Setup Service and Department
    try:
        dept, _ = Department.objects.get_or_create(department_name="TestDept", defaults={"description": "Test", "contact_email": "test@example.com"})
        service, _ = Service.objects.get_or_create(id=2, defaults={
            "service_name": "TestService", 
            "department": dept, 
            "description": "Test", 
            "required_documents": "None",
            "processing_days": 5,
            "fee_amount": 0
        })
        print(f"Service {service.id} ready: {service.service_name}")
    except Exception as e:
        print(f"Error setting up Service: {e}")
        return

    # 3. Create Request
    request = HttpRequest()
    request.method = 'GET'
    request.path = '/citizen/apply/2/'
    request.user = user
    
    # Add messages middleware support
    setattr(request, 'session', {}) # Mock session
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    # 4. Call View
    try:
        print("Calling view...")
        response = views.apply_service(request, service_id=2)
        print(f"Response Status: {response.status_code}")
        if response.status_code != 200:
             print(f"Content: {response.content.decode()[:500]}...") # Print first 500 chars
             
    except Exception as e:
        print("Exception caught during view execution:")
        # traceback.print_exc()
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MSG: {str(e)}")
        if hasattr(e, 'token'):
            print(f"Error at token: {e.token}")


if __name__ == '__main__':
    run()
