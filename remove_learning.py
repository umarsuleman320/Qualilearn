import os
import glob

template_dir = r"c:\Users\Dell\Desktop\Qualilearn\Qualilearn\core\templates"

html_files = glob.glob(os.path.join(template_dir, "*.html"))

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "{% url 'learning' %}" in line:
            print(f"Removed from {os.path.basename(file)}: {line.strip()}")
            # just wrap it in Django comment or remove it. Let's remove it.
            continue
        new_lines.append(line)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Done removing learning links.")
