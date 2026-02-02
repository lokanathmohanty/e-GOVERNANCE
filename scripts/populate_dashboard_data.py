
import os
import django
import random
import sys
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Department, DepartmentCenter, User, LoginHistory, Poll, PollOption, Service

def populate_data():
    print("Starting comprehensive data population...")

    # 1. Update all citizen users with login history
    citizens = User.objects.filter(role='citizen')
    if not citizens.exists():
        print("Creating default citizen user...")
        c = User.objects.create_user(
            username='citizen_tester',
            password='password123',
            email='tester@example.com',
            role='citizen',
            first_name='Citizen',
            last_name='Tester'
        )
        citizens = [c]

    for user in citizens:
        print(f"Populating history for user: {user.username}")
        # Clear old history to ensure fresh data
        LoginHistory.objects.filter(user=user).delete()
        for i in range(5):
            LoginHistory.objects.create(
                user=user,
                ip_address=f"157.24.1.{random.randint(1, 254)}",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
                timestamp=datetime.now() - timedelta(hours=random.randint(1, 100))
            )

    # 2. Departments and Service Centers
    depts_data = [
        {'name': 'Health & Family Welfare', 'desc': 'Medical services and health initiatives.'},
        {'name': 'Revenue & Disaster Management', 'desc': 'Land records and disaster relief.'},
        {'name': 'School & Mass Education', 'desc': 'Education and scholarship services.'},
        {'name': 'Odisha Police', 'desc': 'Law enforcement and public safety.'},
        {'name': 'Panchayati Raj', 'desc': 'Rural development and local governance.'}
    ]

    for d_info in depts_data:
        dept, created = Department.objects.get_or_create(
            department_name=d_info['name'],
            defaults={'description': d_info['desc'], 'contact_email': 'support@odisha.gov.in'}
        )
        # Ensure it's active
        dept.is_active = True
        dept.save()

        # Create service centers if they don't exist
        if not DepartmentCenter.objects.filter(department=dept).exists():
            centers = ['Main Secretariat', 'Regional Hub', 'District Office']
            for c_name in centers:
                DepartmentCenter.objects.create(
                    department=dept,
                    name=f"{dept.department_name} - {c_name}",
                    address=f"{c_name} Complex, Odisha",
                    contact_number="0674-2391234"
                )
                print(f"  Created Center: {dept.department_name} - {c_name}")
        
        # Create services if they don't exist
        if not Service.objects.filter(department=dept).exists():
            Service.objects.create(
                service_name=f"{dept.department_name} Verification",
                department=dept,
                description=f"Standard verification service for {dept.department_name}.",
                required_documents="Aadhaar Card, Proof of Address",
                processing_days=7,
                fee_amount=50.00
            )

    # 3. Polls (Community Voice)
    # Ensure at least one fresh active poll
    Poll.objects.filter(question__icontains="SMART").delete() 
    print("Creating active satisfaction poll...")
    poll = Poll.objects.create(question="How satisfied are you with the new SMART E-Governance Dashboard?", is_active=True)
    options = [
        "Highly Satisfied - It's very fast!", 
        "Satisfied - Good features", 
        "Average - Needs more services", 
        "Not Satisfied - Hard to use"
    ]
    for opt_text in options:
        PollOption.objects.create(poll=poll, text=opt_text, votes=random.randint(5, 50))

    print("Data population complete!")

if __name__ == "__main__":
    populate_data()
