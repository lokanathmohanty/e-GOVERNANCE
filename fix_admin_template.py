
import os
import re

path = r"c:\Users\lokan\OneDrive\Desktop\mejor Project -Render\templates\admin_panel\dashboard.html"
print(f"Fixing file: {path}")

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix 1: The 'else' split
    # Pattern: {% else \n %}history
    # or specifically matches the indentation
    old_block_1 = """{% if 'LOGIN' in log.action %}lock{% elif 'APP' in log.action %}description{% else
                                %}history{% endif %}"""
    new_block_1 = "{% if 'LOGIN' in log.action %}lock{% elif 'APP' in log.action %}description{% else %}history{% endif %}"
    
    if old_block_1 in content:
        content = content.replace(old_block_1, new_block_1)
        print("Fixed Block 1 (history icons)")
    else:
        # Try regex if exact match fails due to spaces
        content = re.sub(r'\{% else\s+%\}(?=history)', '{% else %}', content)
        print("Applied regex for Block 1")

    # Fix 2: The 'Risk: if' split
    old_block_2 = """<span class="text-[8px] font-black text-primary uppercase">Risk: {% if 'fail' in
                                    log.description|lower %}High{% else %}Low{% endif %}</span>"""
    new_block_2 = """<span class="text-[8px] font-black text-primary uppercase">Risk: {% if 'fail' in log.description|lower %}High{% else %}Low{% endif %}</span>"""
    
    if old_block_2 in content:
        content = content.replace(old_block_2, new_block_2)
        print("Fixed Block 2 (Risk label)")
    else:
        # Regex approach for the risk block
        # Match "Risk: {% if 'fail' in" followed by newline and spaces and "log.description"
        pattern = r"(Risk: \{% if 'fail' in)\s+(log\.description\|lower %\})"
        content = re.sub(pattern, r"\1 \2", content)
        print("Applied regex for Block 2")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File updated successfully.")

except Exception as e:
    print(f"Error: {e}")
