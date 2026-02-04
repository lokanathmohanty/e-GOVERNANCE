
import os
import re

path = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates\citizen\track.html"
print(f"Fixing file: {path}")

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic fix for {% else \n %} which seems to be the main culprit
    content = re.sub(r'\{% else\s*\n\s*%\}', '{% else %}', content)
    
    # Fix the specific if split case if generic regex misses or for the 'if' tag split
    # {% if app.status == 'approved' or app.status == 'rejected' \n %}Completed
    content = re.sub(r'(status == \'rejected\')\s*\n\s*%\}', r'\1 %}', content)

    # General cleanup for any tag ending with newline before %}
    # This might be dangerous if not careful, but let's try specific ones first.
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File updated successfully.")

except Exception as e:
    print(f"Error: {e}")
