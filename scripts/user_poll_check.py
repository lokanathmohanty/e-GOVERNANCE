
import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from core.models import User, Poll

def check_users():
    print("--- USERS ---")
    for u in User.objects.all():
        print(f"User: {u.username}, Role: {u.role}, ID: {u.id}")
    
    print("--- POLLS IS_ACTIVE ---")
    for p in Poll.objects.all():
        print(f"Poll: {p.question}, Active: {p.is_active}, ID: {p.id}")

if __name__ == "__main__":
    check_users()
