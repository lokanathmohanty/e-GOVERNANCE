import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Application, User, Department, Service, OfficerAssignment
from django.db.models import Count, Q

def check_stats():
    print("--- Dashboard Data Verification ---")
    
    # Global Stats
    total = Application.objects.count()
    approved = Application.objects.filter(status='approved').count()
    pending = Application.objects.filter(status='pending').count()
    print(f"Total Apps: {total}")
    print(f"Approved: {approved}")
    print(f"Pending: {pending}")

    # Officer Stats
    print("\n--- Officer Performance ---")
    officers = User.objects.filter(role='officer')
    if not officers.exists():
        print("No officers found.")
    for off in officers:
        assignments = OfficerAssignment.objects.filter(officer=off)
        assigned = assignments.count()
        completed = assignments.filter(application__status__in=['approved', 'rejected']).count()
        print(f"Officer: {off.username} | Assigned: {assigned} | Completed: {completed}")

    # Dept Stats
    print("\n--- Department Performance ---")
    dept_stats = Department.objects.annotate(
        app_count=Count('service__application'),
        approved_count=Count('service__application', filter=Q(service__application__status='approved')),
        pending_count=Count('service__application', filter=Q(service__application__status='pending'))
    ).filter(app_count__gt=0)
    
    if not dept_stats.exists():
        print("No departmental application data.")
    for dept in dept_stats:
        print(f"Dept: {dept.department_name} | Total: {dept.app_count} | Approved: {dept.approved_count} | Pending: {dept.pending_count}")

if __name__ == "__main__":
    check_stats()
