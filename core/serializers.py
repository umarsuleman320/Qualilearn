from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Subject, Question, Flashcard, UserProgress, UserProfile,
    VocationalSkill, LearningCategory, LearningTopic, LearningProgress
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'streak_count', 'total_study_minutes', 'last_active_date', 'profile_picture']

class TopicSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = LearningTopic
        fields = ['id', 'name', 'order', 'is_completed']

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LearningProgress.objects.filter(
                user=request.user, topic=obj, is_completed=True
            ).exists()
        return False

class LearningCategorySerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = LearningCategory
        fields = ['id', 'name', 'icon_class', 'order', 'topics', 'percentage']

    def get_percentage(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total = obj.topics.count()
            if total == 0: return 0
            completed = LearningProgress.objects.filter(
                user=request.user, topic__category=obj, is_completed=True
            ).count()
            return round((completed / total) * 100)
        return 0

class SubjectSerializer(serializers.ModelSerializer):
    q_count = serializers.IntegerField(read_only=True)
    fc_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'q_count', 'fc_count']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'explanation']

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'front', 'back']

class AssessmentProgressSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    percentage = serializers.ReadOnlyField()

    class Meta:
        model = UserProgress
        fields = ['id', 'subject', 'subject_name', 'score', 'total_questions', 'completed', 'last_attempt', 'percentage']
