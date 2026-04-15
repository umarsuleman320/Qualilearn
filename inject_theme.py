import os
import glob
tpl_dir = r"c:\Users\Dell\Desktop\Qualilearn\Qualilearn\core\templates"
payload = """<head>
    <script>
        (function() {
            const theme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-bs-theme', theme);
            if(localStorage.getItem('highContrast') === 'true') {
                document.documentElement.classList.add('high-contrast');
            }
            const fs = localStorage.getItem('fontSize');
            if(fs === 'Small') document.documentElement.style.fontSize = '14px';
            else if(fs === 'Large') document.documentElement.style.fontSize = '18px';
            else document.documentElement.style.fontSize = '16px';
        })();
    </script>
    <style>
        .high-contrast { filter: contrast(125%); }
        .high-contrast * { border-color: #000 !important; color: #000 !important; }
        html[data-bs-theme="dark"].high-contrast * { border-color: #fff !important; color: #fff !important; }
    </style>"""

for file in glob.glob(os.path.join(tpl_dir, '*.html')):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<head>' in content and 'localStorage.getItem(\'theme\')' not in content:
        content = content.replace('<head>', payload, 1)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {os.path.basename(file)}')
