
import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Department, DepartmentCenter, Service, Poll, PollOption, User, Application, PollVote

def mega_check():
    print("=== SYSTEM DIAGNOSTIC ===")
    
    # 1. Check DB File
    from django.conf import settings
    db_path = settings.DATABASES['default']['NAME']
    print(f"Database Path: {db_path}")
    print(f"Exists: {os.path.exists(db_path)}")
    
    # 2. Check Models/Data
    print("\n--- Model Counts ---")
    models = [Department, DepartmentCenter, Service, Poll, PollOption, User, Application, PollVote]
    for m in models:
        print(f"{m.__name__}: {m.objects.count()}")

    # 3. Check Active Polls Specifically
    print("\n--- Active Polls ---")
    active_polls = Poll.objects.filter(is_active=True)
    for p in active_polls:
        print(f"Poll: {p.question} (ID: {p.id})")
        opts = p.options.all()
        print(f"  Options ({opts.count()}): {[o.text for o in opts]}")
        if opts.count() == 0:
            print("  WARNING: This poll has no options!")

    # 4. Check Depts/Centers Specifically
    print("\n--- Depts & Centers ---")
    for d in Department.objects.all():
        centers = DepartmentCenter.objects.filter(department=d)
        print(f"Dept: {d.department_name} (ID: {d.id}) -> Centers: {centers.count()}")

    # 5. Check if any Citizen user can see these
    citizen = User.objects.filter(role='citizen').first()
    if citizen:
        print(f"\nTesting for user: {citizen.username}")
        # Test the query used in views
        ap = Poll.objects.filter(is_active=True).first()
        print(f"First active poll for user: {ap}")
        if ap:
            voted = PollVote.objects.filter(user=citizen, poll=ap).exists()
            print(f"Has voted: {voted}")

if __name__ == "__main__":
    mega_check()
