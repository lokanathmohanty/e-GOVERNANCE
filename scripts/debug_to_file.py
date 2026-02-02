
import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import User, Poll

with open('debug_output.txt', 'w') as f:
    f.write("--- USERS ---\n")
    for u in User.objects.all():
        f.write(f"User: {u.username}, Role: {u.role}, ID: {u.id}\n")
    
    f.write("\n--- POLLS ---\n")
    for p in Poll.objects.all():
        f.write(f"Poll: {p.question}, Active: {p.is_active}, ID: {p.id}\n")
