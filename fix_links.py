import os
import re

template_dir = r"C:\Users\Dell\Desktop\Qualilearn\Qualilearn\core\templates"

keyword_to_url = {
    "Dashboard": "{% url 'dashboard' %}",
    "Subjects": "{% url 'learning' %}",
    "Past Questions": "{% url 'assessment' %}",
    "Vocational": "{% url 'vocational' %}",
    "Flashcards": "{% url 'flashcard' %}",
    "Games": "{% url 'games' %}",
    "AI Support": "{% url 'chat' %}",
    "Profile": "{% url 'profile' %}",
    "Settings": "{% url 'settings' %}",
    "Logout": "{% url 'logout' %}",
    "Login": "{% url 'login' %}",
    "Home": "{% url 'home' %}"
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []

    for line in lines:
        original_line = line
        
        # We look for unlinked hrefs: href="#" or href=""
        if 'href="#"' in line or "href='#'" in line:
            for keyword, django_tag in keyword_to_url.items():
                if keyword in line:
                    line = line.replace('href="#"', f'href="{django_tag}"')
                    line = line.replace("href='#'", f'href="{django_tag}"')
                    # Just break out of the loop since we found the match for this line
                    break

        new_lines.append(line)
        if line != original_line:
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated dead links in {os.path.basename(filepath)}")

if __name__ == "__main__":
    for filename in os.listdir(template_dir):
        if filename.endswith(".html"):
            process_file(os.path.join(template_dir, filename))
    print("Done navigating # links.")
