import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualilearn_backend.settings')
django.setup()

from core.models import UserProgress, UserProfile, BroadcastMessage
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def test_dashboard_logic():
    user = User.objects.first()
    if not user:
        print("No user found")
        return

    progress = UserProgress.objects.filter(user=user).order_by('-last_attempt')
    profile, created = UserProfile.objects.get_or_create(user=user)
    today = timezone.localtime().date()
    
    if profile.last_active_date != today:
        if profile.last_active_date == today - timedelta(days=1):
            profile.streak_count += 1
        else:
            profile.streak_count = 1
        profile.last_active_date = today
        profile.save()
        
    streak_word = "on fire — keep it going!"
    if profile.streak_count == 1:
        streak_word = "just sparking — keep building it!"
    elif profile.streak_count >= 5:
        streak_word = "absolutely legendary!"
        
    hours = profile.total_study_minutes // 60
    minutes = profile.total_study_minutes % 60
    study_time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    
    total_score = 0
    total_q = 0
    for p in progress:
        total_score += p.score
        total_q += p.total_questions
    average_score = round((total_score / total_q) * 100) if total_q > 0 else 0

    notifications = BroadcastMessage.objects.all().order_by('-created_at')[:5]
    notification_count = notifications.count()
    
    print(f"Logic works! Notification count: {notification_count}")

if __name__ == "__main__":
    test_dashboard_logic()
