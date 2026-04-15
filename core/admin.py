from django.contrib import admin
from .models import (
    Subject, Question, UserProgress, Flashcard, VocationalSkill, 
    BroadcastMessage, UserProfile, LearningCategory, LearningTopic, LearningProgress
)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count', 'flashcard_count')
    
    def question_count(self, obj):
        return Question.objects.filter(subject=obj).count()
    question_count.short_description = 'Total Questions'

    def flashcard_count(self, obj):
        return Flashcard.objects.filter(subject=obj).count()
    flashcard_count.short_description = 'Total Flashcards'

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text')
    def has_add_permission(self, request):
        return False

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'score', 'total_questions', 'last_attempt')
    list_filter = ('subject', 'last_attempt')
    search_fields = ('user__username', 'subject__name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'streak_count', 'total_study_minutes', 'last_active_date')
    search_fields = ('user__username', 'user__email')

class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('subject', 'front')
    
    def has_add_permission(self, request):
        return False

admin.site.register(Flashcard, FlashcardAdmin)

@admin.register(VocationalSkill)
class VocationalSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'youtube_url')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent')
    
    def save_model(self, request, obj, form, change):
        if not obj.sent:
            from django.core.mail import send_mass_mail
            from django.contrib.auth.models import User
            
            users = User.objects.exclude(email='')
            messages = []
            for user in users:
                messages.append(
                    (obj.subject, obj.message, 'admin@qualilearn.com', [user.email])
                )
            
            if messages:
                send_mass_mail(tuple(messages), fail_silently=False)
            
            obj.sent = True

class LearningTopicInline(admin.TabularInline):
    model = LearningTopic
    extra = 1

@admin.register(LearningCategory)
class LearningCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'topic_count')
    inlines = [LearningTopicInline]
    
    def topic_count(self, obj):
        return obj.topics.count()

@admin.register(LearningTopic)
class LearningTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'topic__category')
    search_fields = ('user__username', 'topic__name')
