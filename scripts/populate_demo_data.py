import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Application, User, Department, Service, OfficerAssignment

def populate():
    print("Populating demo data...")
    
    # Ensure we have departments
    depts = Department.objects.all()
    if not depts.exists():
        print("Creating default departments...")
        depts = [
            Department.objects.create(department_name="Ministry of Revenue", description="Handles land and tax services"),
            Department.objects.create(department_name="Digital Odisha Office", description="Handles IT and e-Governance"),
            Department.objects.create(department_name="Welfare Department", description="Social schemes and benefits")
        ]
    
    # Ensure we have services
    services = Service.objects.all()
    if not services.exists():
        print("Creating default services...")
        services = [
            Service.objects.create(service_name="Residential Certificate", department=depts[0], processing_days=15),
            Service.objects.create(service_name="Income Certificate", department=depts[0], processing_days=10),
            Service.objects.create(service_name="Digital ID Issuance", department=depts[1], processing_days=5),
            Service.objects.create(service_name="Pension Enrollment", department=depts[2], processing_days=30)
        ]

    # Ensure we have officers
    officers = User.objects.filter(role='officer')
    if not officers.exists():
        print("Creating demo officers...")
        for i in range(1, 4):
            User.objects.create_user(
                username=f"officer_{i}",
                password="Password@123",
                role="officer",
                first_name=f"Officer",
                last_name=str(i)
            )
        officers = User.objects.filter(role='officer')

    # Ensure we have a citizen
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        print("Creating demo citizen...")
        citizen = User.objects.create_user(
            username="citizen_demo",
            password="Password@123",
            role="citizen",
            first_name="John",
            last_name="Citizen"
        )

    # Create applications if few exist
    if Application.objects.count() < 10:
        print("Creating 15 demo applications...")
        statuses = ['pending', 'approved', 'rejected', 'under_review']
        for i in range(15):
            svc = random.choice(services)
            app = Application.objects.create(
                user=citizen,
                service=svc,
                status=random.choice(statuses),
                application_number=f"APP-{random.randint(10000, 99999)}",
                applied_date=timezone.now() - timedelta(days=random.randint(1, 60))
            )
            
            # Setup deadlines
            app.sla_deadline = app.applied_date + timedelta(days=svc.processing_days)
            if app.status in ['approved', 'rejected']:
                app.approved_date = app.applied_date + timedelta(days=random.randint(1, svc.processing_days))
            app.save()

            # Randomly assign to officers
            if random.random() > 0.3:
                off = random.choice(officers)
                OfficerAssignment.objects.get_or_create(application=app, officer=off)

    print("Success! Dashboard should now have data.")

if __name__ == "__main__":
    populate()
