
import os

path = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates\base.html"
print(f"Fixing file: {path}")

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is specifically in lines 227-229 where comparison operators lack whitespace
    # {% if user.role=='citizen' %} => {% if user.role == 'citizen' %}
    
    # Let's replace the whole affected block with a clean, single-line version
    
    old_block_start = '{% if user.role==\'citizen\' %}data-i18n="dashboard"'
    
    # Since previous attempts might have partially worked or failed due to multiline matching
    # I'll use a more aggressive approach to find the broken tag area.
    
    # We look for the data-i18n block for the dashboard link
    
    # Target string segments from the error log "user.role=='citizen'"
    
    content = content.replace("user.role=='citizen'", "user.role == 'citizen'")
    content = content.replace("user.role=='officer'", "user.role == 'officer'")
    content = content.replace("user.role=='department_head'", "user.role == 'department_head'")
    
    # Also handle the multiline split if it exists
    # If previous replace_file_content failed, the file content is likely still the same
    # or partially modified.
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File updated successfully.")

except Exception as e:
    print(f"Error: {e}")
