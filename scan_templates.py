
import os
import re

root_dir = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates"

print("Scanning for split template tags in templates directory...")

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            path = os.path.join(dirpath, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for split tags: {% ... \n ... %}
                # We specifically look for cases where the tag content is split across lines unpredictably
                # but valid django tags can be multiline.
                # The issue we saw was split 'else' or 'if' causing syntax errors because of how they were written
                
                # Look for split 'else' specifically: {% else \n %}
                if re.search(r'\{% else\s*\n\s*%\}', content):
                    print(f"SUSPICIOUS ELSE in: {path}")
                    
                # Look for split 'endif': {% endif \n %} (unlikely key issue but checking)
                
                # Look for the specific broken if/else structure we saw
                # {% if ... %}\n ... {% else \n %} ... {% endif %}
                
                # Just general check for {% else followed by newline
                
            except Exception as e:
                print(f"Error reading {path}: {e}")
