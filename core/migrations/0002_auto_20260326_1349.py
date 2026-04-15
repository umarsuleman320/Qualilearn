from django.db import migrations

def create_subjects_and_topics(apps, schema_editor):
    Subject = apps.get_model('core', 'Subject')
    Topic = apps.get_model('core', 'Topic')

    # Create Subjects
    math, _ = Subject.objects.get_or_create(name="Mathematics")
    physics, _ = Subject.objects.get_or_create(name="Physics")
    chemistry, _ = Subject.objects.get_or_create(name="Chemistry")
    biology, _ = Subject.objects.get_or_create(name="Biology")

    # Create Topics
    Topic.objects.get_or_create(subject=math, name="Quadratic Equations")
    Topic.objects.get_or_create(subject=math, name="Algebra")
    Topic.objects.get_or_create(subject=physics, name="Simple Harmonic Motion")
    Topic.objects.get_or_create(subject=physics, name="Projectile Motion")
    Topic.objects.get_or_create(subject=chemistry, name="Periodic Table")
    Topic.objects.get_or_create(subject=chemistry, name="Chemical Bonding")
    Topic.objects.get_or_create(subject=biology, name="Cell Structure")
    Topic.objects.get_or_create(subject=biology, name="Photosynthesis")

    print("Subjects and Topics created successfully!")

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),   # Change this number if your first migration has a different name
    ]

    operations = [
        migrations.RunPython(create_subjects_and_topics),
    ]