
import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Department, DepartmentCenter, Poll, Service, User

def check_data():
    print("--- DATA CHECK ---")
    print(f"Departments: {Department.objects.count()}")
    for d in Department.objects.all():
        print(f"  - {d.department_name} (ID: {d.id})")
        centers = DepartmentCenter.objects.filter(department=d)
        print(f"    Centers: {centers.count()}")
        for c in centers:
            print(f"      * {c.name} (ID: {c.id})")
            
    print(f"Services: {Service.objects.count()}")
    print(f"Polls (Total): {Poll.objects.count()}")
    print(f"Polls (Active): {Poll.objects.filter(is_active=True).count()}")
    
    active_poll = Poll.objects.filter(is_active=True).first()
    if active_poll:
        print(f"Active Poll: {active_poll.question}")
        print(f"Options: {active_poll.options.count()}")

if __name__ == "__main__":
    check_data()
