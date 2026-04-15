import os
import glob

template_dir = r"c:\Users\Dell\Desktop\Qualilearn\Qualilearn\core\templates"
html_files = glob.glob(os.path.join(template_dir, "*.html"))

for file in html_files:
    basename = os.path.basename(file)
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Only process if learning is NOT in the file already
    if any("{% url 'learning' %}" in line for line in lines):
        continue

    new_lines = []
    
    for i, line in enumerate(lines):
        if "{% url 'assessment' %}" in line and "nav-link" in line:
            # We found the line where 'assessment' is linked. 
            # We need to insert the learning link before this line.
            leading_whitespace = line[:len(line) - len(line.lstrip())]
            
            # Decide on the exact string based on earlier logs
            if basename == "base.html":
                learning_line = f'{leading_whitespace}<li class="nav-item"><a class="nav-link" href="{{% url \'learning\' %}}"><i class="bi bi-journal-bookmark-fill me-2"></i> Subjects</a></li>\n'
            elif basename == "learning.html":
                learning_line = f'{leading_whitespace}<li class="nav-item"><a class="nav-link active" href="{{% url \'learning\' %}}"><i class="bi bi-book-half me-2"></i> Subjects</a></li>\n'
            else:
                learning_line = f'{leading_whitespace}<li class="nav-item"><a class="nav-link" href="{{% url \'learning\' %}}"><i class="bi bi-book-half me-2"></i> Subjects</a></li>\n'
                
            new_lines.append(learning_line)
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
print("Restored learning links.")
