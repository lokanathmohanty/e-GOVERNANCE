
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
    print("Starting data population...")

    # 1. Ensure at least one citizen user exists for dummy data
    user = User.objects.filter(role='citizen').first()
    if not user:
        print("Creating citizen user...")
        user = User.objects.create_user(
            username='citizen_test',
            password='password123',
            email='citizen@example.com',
            role='citizen',
            first_name='Test',
            last_name='Citizen'
        )

    # 2. Departments and Service Centers
    depts_data = [
        {'name': 'Health & Family Welfare', 'desc': 'Medical services and health initiatives.'},
        {'name': 'Revenue & Disaster Management', 'desc': 'Land records and disaster relief.'},
        {'name': 'School & Mass Education', 'desc': 'Education and scholarship services.'},
        {'name': 'Odisha Police', 'desc': 'Law enforcement and public safety.'}
    ]

    for d_info in depts_data:
        dept, created = Department.objects.get_or_create(
            department_name=d_info['name'],
            defaults={'description': d_info['desc'], 'contact_email': 'contact@odisha.gov.in'}
        )
        if created:
            print(f"Created Department: {dept.department_name}")
            # Create a few service centers for each department
            centers = ['Central Unit', 'Regional Office', 'District Hub']
            for c_name in centers:
                DepartmentCenter.objects.create(
                    department=dept,
                    name=f"{dept.department_name} - {c_name}",
                    address=f"Bhubaneswar, Odisha",
                    contact_number="0674-1234567"
                )
                print(f"  Created Center: {dept.department_name} - {c_name}")
            
            # Also create some services if none exist
            if not dept.services.exists():
                Service.objects.create(
                    service_name=f"General {dept.department_name} Support",
                    department=dept,
                    description=f"General support for {dept.department_name}",
                    required_documents="ID Proof",
                    processing_days=7
                )

    # 3. Login History (Security Wall)
    if not LoginHistory.objects.filter(user=user).exists():
        print(f"Creating login history for {user.username}...")
        for i in range(5):
            LoginHistory.objects.create(
                user=user,
                ip_address=f"192.168.1.{random.randint(1, 254)}",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
                timestamp=datetime.now() - timedelta(days=i)
            )

    # 4. Polls (Community Voice)
    if not Poll.objects.filter(is_active=True).exists():
        print("Creating satisfaction poll...")
        poll = Poll.objects.create(question="Overall Satisfaction with SMART Odisha Portal")
        options = ["Extremely Satisfied", "Satisfied", "Needs Improvement", "Poor Experience"]
        for opt_text in options:
            PollOption.objects.create(poll=poll, text=opt_text, votes=random.randint(10, 100))

    print("Data population complete!")

if __name__ == "__main__":
    populate_data()
