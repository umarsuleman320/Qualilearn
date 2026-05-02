from django.contrib import admin
from django.urls import path, include
from core import views, api_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main Pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/', views.chat, name='chat'),
    path('assessment/', views.assessment, name='assessment'),
    path('start-assessment/', views.start_assessment, name='start_assessment'),
    path('take-assessment/', views.take_assessment, name='take_assessment'),
    path('submit-assessment/', views.submit_assessment, name='submit_assessment'),
    
    path('learning/', views.learning, name='learning'),
    path('api/toggle-learning/', views.toggle_learning_completion, name='toggle_learning'),
    path('flashcard/', views.flashcard, name='flashcard'),
    path('start-flashcard/', views.start_flashcard, name='start_flashcard'),
    path('take-flashcard/', views.take_flashcard, name='take_flashcard'),
    path('games/', views.games, name='games'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('vocational/', views.vocational, name='vocational'),
    
    # Mobile API v1
    path('api/v1/auth/login/', api_views.MobileLoginView.as_view(), name='api_login'),
    path('api/v1/auth/logout/', api_views.MobileLogoutView.as_view(), name='api_logout'),
    path('api/v1/syllabus/', api_views.SyllabusListView.as_view(), name='api_syllabus'),
    path('api/v1/syllabus/toggle/<int:topic_id>/', api_views.ToggleTopicCompletionView.as_view(), name='api_toggle'),
    path('api/v1/subjects/', api_views.SubjectListView.as_view(), name='api_subjects'),
    path('api/v1/subjects/<int:subject_id>/questions/', api_views.QuestionListView.as_view(), name='api_questions'),
    path('api/v1/subjects/<int:subject_id>/flashcards/', api_views.FlashcardListView.as_view(), name='api_flashcards'),
    path('api/v1/profile/', api_views.UserProfileView.as_view(), name='api_profile'),
    
    # AI Chat API
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)