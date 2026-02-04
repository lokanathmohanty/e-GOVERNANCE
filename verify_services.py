
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateSyntaxError

try:
    print("Attempting to load services template...")
    t = get_template('citizen/services_bootstrap.html')
    print("Services Template parsed successfully!")
except TemplateSyntaxError as e:
    print(f"TEMPLATE SYNTAX ERROR: {e}")
    if hasattr(e, 'token'):
        print(f"Error at token: {e.token}")
except Exception as e:
    print(f"OTHER ERROR: {e}")
