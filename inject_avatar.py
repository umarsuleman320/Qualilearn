import os
import glob
import re

tpl_dir = r"c:\Users\Dell\Desktop\Qualilearn\Qualilearn\core\templates"
replacement = """<div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold overflow-hidden" style="width:42px;height:42px;">
                                {% if request.user.userprofile.profile_picture %}
                                <img src="{{ request.user.userprofile.profile_picture.url }}" alt="{{ request.user.first_name }}" class="w-100 h-100 object-fit-cover">
                                {% else %}
                                {{ request.user.first_name|make_list|first|default:"U"|upper }}
                                {% endif %}
                            </div>"""

pattern = re.compile(r'<div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold" style="width:42px;height:42px;">\s*U\s*</div>', re.DOTALL)
pattern_name = re.compile(r'<span class="d-none d-md-inline fw-medium">Umar</span>')

for filepath in glob.glob(os.path.join(tpl_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = pattern.sub(replacement, content)
    new_content = pattern_name.sub('<span class="d-none d-md-inline fw-medium">{{ request.user.first_name|default:"User" }}</span>', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated avatar logic in {os.path.basename(filepath)}')
