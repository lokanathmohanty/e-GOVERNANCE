
import os
import re

path = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates\citizen\apply_form_bootstrap.html"
print(f"Fixing file: {path}")

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix split else tag
    # The pattern we saw: {% else \n %}Free
    fixed_content = re.sub(r'\{% else\s+%\}(?=Free)', '{% else %}', content)
    
    # Also generic fix for broken tags spanning lines where delimiters are split
    # This is hard to regex perfectly but let's try specific known issues
    
    # Fix the specific fee line
    if '{% else\n' in content and '%}Free' in content:
        print("Found split else tag, fixing...")
        fixed_content = fixed_content.replace('{% else\n                                    %}Free', '{% else %}Free')
    
    # Fix the priority lines
    # Pattern: id="priorityNormal" {% if not existing_app or\n existing_app.priority=="normal" %}
    fixed_content = re.sub(r'(\{% if.*?)\n\s+(.*?\%\})', r'\1 \2', fixed_content)

    if content != fixed_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("File updated successfully.")
    else:
        print("No changes needed (or regex failed to match).")
        
except Exception as e:
    print(f"Error: {e}")
