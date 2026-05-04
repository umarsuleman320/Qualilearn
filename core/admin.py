from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Subject, Question, UserProgress, Flashcard, VocationalSkill,
    BroadcastMessage, UserProfile, LearningCategory, LearningTopic, LearningProgress
)


# ============================================================
# LEARNING TOPIC INLINE — shown inside a Subject's edit page
# Add as many topics as you want at once (name + YouTube link)
# ============================================================
class LearningTopicInline(admin.TabularInline):
    model = LearningTopic
    extra = 5          # 5 empty rows so you can add many at once
    min_num = 0
    can_delete = True
    fields = ('name', 'youtube_url', 'order')
    verbose_name = "Topic"
    verbose_name_plural = "Topics  (add as many as you like at once)"


# ============================================================
# SUBJECT INLINE — shown inside a Category edit page
# Click "Change" arrow to open the Subject and add its Topics
# ============================================================
class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1
    fields = ('name',)
    show_change_link = True   # ← click the arrow to open Subject page → add topics there
    verbose_name = "Subject"
    verbose_name_plural = "Subjects  (click the ↗ arrow to open a Subject and add its Topics)"


# ============================================================
# LEARNING CATEGORY ADMIN
# Structure:  Category → (inline) Subjects  →  Topics per Subject
# ============================================================
@admin.register(LearningCategory)
class LearningCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'subject_count')
    ordering = ('order', 'name')
    inlines = [SubjectInline]

    def subject_count(self, obj):
        return obj.subjects.count()
    subject_count.short_description = 'Subjects'


# ============================================================
# SUBJECT ADMIN — the main page for adding topics
# Workflow: pick Category → type Subject name → add topics below
# ============================================================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'topic_count', 'question_count', 'flashcard_count')
    list_filter = ('category',)
    list_select_related = ('category',)
    search_fields = ('name',)
    ordering = ('category__order', 'name')

    # ---- fieldsets: Category + Subject name at top, then documents ----
    fieldsets = (
        ('📚 Subject Details', {
            'description': (
                'Choose the category this subject belongs to, give it a name, '
                'then scroll down to add its topics with YouTube links.'
            ),
            'fields': ('category', 'name'),
        }),
        ('📄 Question & Flashcard Files (optional)', {
            'classes': ('collapse',),
            'fields': ('document', 'flashcard_document'),
        }),
    )

    inlines = [LearningTopicInline]

    def topic_count(self, obj):
        return obj.learning_topics.count()
    topic_count.short_description = 'Topics'

    def question_count(self, obj):
        from .models import Question
        return Question.objects.filter(subject=obj).count()
    question_count.short_description = 'Questions'

    def flashcard_count(self, obj):
        return Flashcard.objects.filter(subject=obj).count()
    flashcard_count.short_description = 'Flashcards'


# ============================================================
# LEARNING TOPIC ADMIN (standalone list — read-only friendly)
# ============================================================
@admin.register(LearningTopic)
class LearningTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'category_name', 'youtube_link', 'order')
    list_filter = ('subject__category', 'subject')
    search_fields = ('name', 'subject__name')
    list_select_related = ('subject', 'subject__category')
    ordering = ('subject__category__order', 'subject__name', 'order')

    # When adding/editing a single topic, show subject + category info clearly
    fieldsets = (
        ('Topic Info', {
            'description': (
                'Tip: It is faster to add many topics at once by opening the Subject page '
                '(Admin → Core → Subjects → pick a subject) and filling in the inline rows.'
            ),
            'fields': ('subject', 'name', 'youtube_url', 'order'),
        }),
    )

    def category_name(self, obj):
        return obj.subject.category.name if obj.subject and obj.subject.category else '—'
    category_name.short_description = 'Category'

    def youtube_link(self, obj):
        if obj.youtube_url:
            return format_html('<a href="{}" target="_blank">▶ Watch</a>', obj.youtube_url)
        return '—'
    youtube_link.short_description = 'YouTube'


# ============================================================
# QUESTION ADMIN
# ============================================================
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text')
    def has_add_permission(self, request):
        return False

admin.site.register(Question, QuestionAdmin)


# ============================================================
# USER PROGRESS ADMIN
# ============================================================
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'score', 'total_questions', 'last_attempt')
    list_filter = ('subject', 'last_attempt')
    search_fields = ('user__username', 'subject__name')


# ============================================================
# USER PROFILE ADMIN
# ============================================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'streak_count', 'total_study_minutes', 'last_active_date')
    search_fields = ('user__username', 'user__email')


# ============================================================
# FLASHCARD ADMIN
# ============================================================
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('subject', 'front')
    def has_add_permission(self, request):
        return False

admin.site.register(Flashcard, FlashcardAdmin)


# ============================================================
# VOCATIONAL SKILL ADMIN
# ============================================================
@admin.register(VocationalSkill)
class VocationalSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'youtube_url')
    list_filter = ('category',)
    search_fields = ('name',)


# ============================================================
# BROADCAST MESSAGE ADMIN
# ============================================================
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
        super().save_model(request, obj, form, change)


# ============================================================
# LEARNING PROGRESS ADMIN
# ============================================================
@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('user__username', 'topic__name')
