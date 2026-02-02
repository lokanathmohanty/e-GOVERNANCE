
import os
import django
import sys
import random
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Department, DepartmentCenter, Service, Poll, PollOption, User, Application

def cleanup_and_populate():
    print("--- CLEANING UP ---")
    Poll.objects.all().delete()
    DepartmentCenter.objects.all().delete()
    # Not deleting Departments or Services to avoid breaking applications
    
    # 1. Ensure at least one poll exists and is active
    print("--- CREATING POLL ---")
    poll = Poll.objects.create(question="How satisfied are you with the new SMART E-Governance Dashboard?", is_active=True)
    options = ["Extremely Satisfied", "Very Good", "Needs Improvement", "Not Satisfied"]
    for opt_text in options:
        PollOption.objects.create(poll=poll, text=opt_text, votes=random.randint(50, 200))
    print(f"Created Poll: {poll.question} (ID: {poll.id})")

    # 2. Ensure Departments have Centers
    print("--- ENSURING CENTERS ---")
    all_depts = Department.objects.all()
    if not all_depts.exists():
        d1 = Department.objects.create(department_name="Health & Family Welfare", contact_email="health@odisha.gov.in")
        d2 = Department.objects.create(department_name="Odisha Police", contact_email="police@odisha.gov.in")
        all_depts = [d1, d2]
    
    for dept in all_depts:
        # Create 2 centers per dept
        c1 = DepartmentCenter.objects.create(
            department=dept,
            name=f"{dept.department_name} - Coastal Office",
            address="Bhubaneswar, Odisha",
            contact_number="0674-123456"
        )
        c2 = DepartmentCenter.objects.create(
            department=dept,
            name=f"{dept.department_name} - Western Hub",
            address="Sambalpur, Odisha",
            contact_number="0663-123456"
        )
        print(f"Created 2 centers for {dept.department_name}")

    # 3. Ensure Services exist
    if not Service.objects.exists():
        for dept in all_depts:
            Service.objects.create(
                service_name=f"General {dept.department_name} Helpdesk",
                department=dept,
                description="Assistance with department services",
                required_documents="ID Card",
                processing_days=3
            )
        print("Created services")

    print("--- DATA SETUP COMPLETE ---")

if __name__ == "__main__":
    cleanup_and_populate()
