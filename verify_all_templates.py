
import os
import django
from django.conf import settings

# Configure Django settings (minimal needed for template loading)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egovernance.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateSyntaxError, TemplateDoesNotExist

def verify_all_templates():
    base_dir = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates"
    errors_found = []
    
    print(f"Scanning templates in {base_dir}...")
    
    count = 0
    success = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                count += 1
                # Calculate relative path for loader, e.g. "citizen/apply.html"
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                # Normalize slashes for Django
                template_name = rel_path.replace(os.sep, '/')
                
                try:
                    get_template(template_name)
                    success += 1
                except TemplateSyntaxError as e:
                    errors_found.append(f"SYNTAX ERROR in {template_name}: {e}")
                except TemplateDoesNotExist:
                    # Sometimes relative includes might be tricky, or partials
                    # But get_template should find files if they exist in valid dirs
                    errors_found.append(f"DOES NOT EXIST (Loader failed): {template_name}")
                except Exception as e:
                    errors_found.append(f"OTHER ERROR in {template_name}: {e}")

    print(f"\nScan Complete.")
    print(f"Total Templates: {count}")
    print(f"Successful Load: {success}")
    print(f"Errors Found: {len(errors_found)}")
    
    if errors_found:
        print("\n--- ERROR DETAILS ---")
        for err in errors_found:
            print(err)

if __name__ == '__main__':
    verify_all_templates()
