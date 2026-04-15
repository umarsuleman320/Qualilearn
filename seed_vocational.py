import os
import django
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualilearn_backend.settings')
django.setup()

from core.models import VocationalSkill

skills_data = [
    # Practical Skills
    {"name": "Small chops / snacks making", "category": "Practical Skills", "icon": "bi-egg-fried"},
    {"name": "Catering (basic cooking)", "category": "Practical Skills", "icon": "bi-cup-hot"},
    {"name": "Hair braiding", "category": "Practical Skills", "icon": "bi-scissors"},
    {"name": "Barbing", "category": "Practical Skills", "icon": "bi-scissors"},
    {"name": "Laundry services", "category": "Practical Skills", "icon": "bi-droplet"},
    {"name": "Perfume oil making", "category": "Practical Skills", "icon": "bi-flower1"},
    {"name": "Liquid soap making", "category": "Practical Skills", "icon": "bi-droplet-half"},
    {"name": "Cake baking (small scale)", "category": "Practical Skills", "icon": "bi-heart"},
    {"name": "Phone accessories sales", "category": "Practical Skills", "icon": "bi-phone"},
    {"name": "Car washing", "category": "Practical Skills", "icon": "bi-car-front"},

    # Soft / Digital Skills
    {"name": "Graphics design", "category": "Soft / Digital Skills", "icon": "bi-palette"},
    {"name": "Data analysis", "category": "Soft / Digital Skills", "icon": "bi-bar-chart"},
    {"name": "Frontend web development", "category": "Soft / Digital Skills", "icon": "bi-code-slash"},
    {"name": "Social media management", "category": "Soft / Digital Skills", "icon": "bi-share"},
    {"name": "Content writing", "category": "Soft / Digital Skills", "icon": "bi-pen"},
    {"name": "Video editing", "category": "Soft / Digital Skills", "icon": "bi-film"},
    {"name": "UI/UX design (basic)", "category": "Soft / Digital Skills", "icon": "bi-vector-pen"},
    {"name": "Digital marketing", "category": "Soft / Digital Skills", "icon": "bi-megaphone"},
    {"name": "Virtual assistance", "category": "Soft / Digital Skills", "icon": "bi-headset"},
    {"name": "Basic project management", "category": "Soft / Digital Skills", "icon": "bi-kanban"},
]

print("Clearing old vocational skills...")
VocationalSkill.objects.all().delete()

print("Seeding new vocational skills and generating YouTube links...")
for skill in skills_data:
    query = urllib.parse.quote_plus(skill['name'] + " tutorial for beginners")
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    VocationalSkill.objects.create(
        name=skill['name'],
        category=skill['category'],
        youtube_url=youtube_url,
        icon_class=skill['icon']
    )

print(f"Successfully seeded {len(skills_data)} vocational skills!")
