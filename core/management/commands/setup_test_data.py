from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Service, SystemConfiguration
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with initial test data including users, departments, and services'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # 1. Create System Configuration
        if not SystemConfiguration.objects.exists():
            SystemConfiguration.objects.create(
                environment='prod',
                maintenance_mode=False,
                portal_name='Smart Odisha - e-Governance',
                system_version='3.0.0-Release'
            )
            self.stdout.write(self.style.SUCCESS('System Configuration created.'))

        # 2. Create Users
        users = [
            {
                'username': 'admin',
                'password': 'Password@123',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@odisha.gov.in',
                'first_name': 'System',
                'last_name': 'Administrator'
            },
            {
                'username': 'officer1',
                'password': 'Password@123',
                'role': 'officer',
                'is_staff': True,
                'is_superuser': False,
                'email': 'officer1@odisha.gov.in',
                'first_name': 'Rajesh',
                'last_name': 'Mohanty'
            },
            {
                'username': 'head1',
                'password': 'Password@123',
                'role': 'department_head',
                'is_staff': True,
                'is_superuser': False,
                'email': 'head1@odisha.gov.in',
                'first_name': 'Arun',
                'last_name': 'Patnaik'
            },
            {
                'username': 'final_tester',
                'password': 'Password@123',
                'role': 'citizen',
                'is_staff': False,
                'is_superuser': False,
                'email': 'tester@odisha.gov.in',
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'aadhaar_number': '123456789012'
            }
        ]

        for user_data in users:
            username = user_data.pop('username')
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(username=username, defaults=user_data)
            if created or not user.check_password(password):
                user.set_password(password)
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User {username} created/updated.'))

        # 3. Create Departments
        depts_data = [
            {
                'name': 'Revenue & Disaster Management',
                'desc': 'Handles land records, certificates, and disaster relief.',
                'email': 'revenue@odisha.gov.in'
            },
            {
                'name': 'Food & Civil Supplies',
                'desc': 'Manages PDS, Ration cards, and essential commodities.',
                'email': 'food@odisha.gov.in'
            },
            {
                'name': 'General Administration',
                'desc': 'Human resources and administrative services.',
                'email': 'ga@odisha.gov.in'
            },
            {
                'name': 'Transport Department',
                'desc': 'Vehicle registration and licensing services.',
                'email': 'transport@odisha.gov.in'
            }
        ]

        head_user = User.objects.get(username='head1')
        departments = {}
        for d in depts_data:
            dept, created = Department.objects.get_or_create(
                department_name=d['name'],
                defaults={
                    'description': d['desc'],
                    'contact_email': d['email'],
                    'head_officer': head_user
                }
            )
            departments[d['name']] = dept
            if created:
                self.stdout.write(self.style.SUCCESS(f'Department {d["name"]} created.'))

        # 4. Create Services
        services_data = [
            {
                'name': 'Income Certificate',
                'dept': 'Revenue & Disaster Management',
                'days': 15,
                'fee': 30.00,
                'docs': 'Aadhaar, Identity Proof, Salary Certificate'
            },
            {
                'name': 'Residential Certificate',
                'dept': 'Revenue & Disaster Management',
                'days': 10,
                'fee': 20.00,
                'docs': 'Aadhaar, Land Records, Ration Card'
            },
            {
                'name': 'Caste Certificate',
                'dept': 'Revenue & Disaster Management',
                'days': 30,
                'fee': 50.00,
                'docs': 'Community Proof, Father\'s Certificate'
            },
            {
                'name': 'Ration Card Application',
                'dept': 'Food & Civil Supplies',
                'days': 45,
                'fee': 0.00,
                'docs': 'Family Income, Head of Family ID'
            },
            {
                'name': 'Driving License Renewal',
                'dept': 'Transport Department',
                'days': 7,
                'fee': 500.00,
                'docs': 'Old License, Medical Fitness'
            }
        ]

        for s in services_data:
            service, created = Service.objects.get_or_create(
                service_name=s['name'],
                department=departments[s['dept']],
                defaults={
                    'description': f"Official service for {s['name']}",
                    'processing_days': s['days'],
                    'fee_amount': s['fee'],
                    'required_documents': s['docs'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Service {s["name"]} created.'))

        self.stdout.write(self.style.SUCCESS('Verification: Database is now ready for testing.'))
