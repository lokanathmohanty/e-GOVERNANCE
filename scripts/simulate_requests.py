import os
import django
import sys
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from citizen.views import book_appointment, dashboard

def simulate_requests():
    User = get_user_model()
    user = User.objects.filter(role='citizen').first()
    if not user:
        print("No citizen user found to test.")
        return

    factory = RequestFactory()
    
    # Test Dashboard
    print(f"\n--- Testing Dashboard for {user.username} ---")
    request = factory.get(reverse('citizen:dashboard'))
    request.user = user
    try:
        response = dashboard(request)
        print(f"Status: {response.status_code}")
        # Print if there's an error message in context
        if hasattr(response, 'context_data'):
             print(f"Context Error: {response.context_data.get('error_message')}")
        else:
             # For TemplateResponse/Response, check content if it's there
             pass
    except Exception as e:
        print(f"Dashboard Failed: {str(e)}")

    # Test Book Appointment
    print(f"\n--- Testing Book Appointment for {user.username} ---")
    request = factory.get(reverse('citizen:book_appointment'))
    request.user = user
    try:
        response = book_appointment(request)
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Book Appointment Failed: {str(e)}")

if __name__ == "__main__":
    simulate_requests()
