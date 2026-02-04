
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateSyntaxError

try:
    print("Attempting to load admin dashboard template...")
    # Note: path might need to be relative to template dirs
    t = get_template('admin_panel/dashboard.html')
    print("Admin Dashboard Template parsed successfully!")
except TemplateSyntaxError as e:
    print(f"TEMPLATE SYNTAX ERROR: {e}")
    if hasattr(e, 'token'):
        print(f"Error at token: {e.token}")
except Exception as e:
    print(f"OTHER ERROR: {e}")
