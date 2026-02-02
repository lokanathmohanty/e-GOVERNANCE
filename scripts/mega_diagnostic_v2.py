
import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import Department, DepartmentCenter, Service, Poll, PollOption, User, Application, PollVote

with open('mega_diagnostic.txt', 'w') as f:
    f.write("=== SYSTEM DIAGNOSTIC ===\n")
    
    # 1. Check DB File
    from django.conf import settings
    db_path = str(settings.DATABASES['default']['NAME'])
    f.write(f"Database Path: {db_path}\n")
    f.write(f"Exists: {os.path.exists(db_path)}\n")
    
    # 2. Check Models/Data
    f.write("\n--- Model Counts ---\n")
    models_to_check = [Department, DepartmentCenter, Service, Poll, PollOption, User, Application, PollVote]
    for m in models_to_check:
        f.write(f"{m.__name__}: {m.objects.count()}\n")

    # 3. Check Active Polls Specifically
    f.write("\n--- Active Polls ---\n")
    active_polls = Poll.objects.filter(is_active=True)
    for p in active_polls:
        f.write(f"Poll: {p.question} (ID: {p.id})\n")
        opts = p.options.all()
        f.write(f"  Options ({opts.count()}): {[o.text for o in opts]}\n")
        if opts.count() == 0:
            f.write("  WARNING: This poll has no options!\n")

    # 4. Check Depts/Centers Specifically
    f.write("\n--- Depts & Centers ---\n")
    for d in Department.objects.all():
        centers = DepartmentCenter.objects.filter(department=d)
        f.write(f"Dept: {d.department_name} (ID: {d.id}) -> Centers: {centers.count()}\n")

    # 5. Check if any Citizen user can see these
    citizen = User.objects.filter(role='citizen').first()
    if citizen:
        f.write(f"\nTesting for user: {citizen.username}\n")
        # Test the query used in views
        ap = Poll.objects.filter(is_active=True).first()
        f.write(f"First active poll for user: {ap}\n")
        if ap:
            voted = PollVote.objects.filter(user=citizen, poll=ap).exists()
            f.write(f"Has voted: {voted}\n")
