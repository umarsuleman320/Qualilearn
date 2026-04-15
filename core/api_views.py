from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count
from .models import (
    Subject, Question, Flashcard, UserProgress, UserProfile,
    LearningCategory, LearningTopic, LearningProgress
)
from .serializers import (
    UserSerializer, UserProfileSerializer, SubjectSerializer,
    QuestionSerializer, FlashcardSerializer, LearningCategorySerializer,
    AssessmentProgressSerializer
)

class MobileLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class MobileLogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SyllabusListView(generics.ListAPIView):
    queryset = LearningCategory.objects.all().prefetch_related('topics')
    serializer_class = LearningCategorySerializer

class ToggleTopicCompletionView(APIView):
    def post(self, request, topic_id):
        try:
            topic = LearningTopic.objects.get(id=topic_id)
            progress, created = LearningProgress.objects.get_or_create(user=request.user, topic=topic)
            is_completed = request.data.get('is_completed', not progress.is_completed)
            progress.is_completed = is_completed
            progress.save()
            return Response({'status': 'success', 'is_completed': is_completed})
        except LearningTopic.DoesNotExist:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.annotate(
            q_count=Count('question', distinct=True),
            fc_count=Count('flashcard', distinct=True)
        )

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Question.objects.filter(subject_id=subject_id).order_by('?')

class FlashcardListView(generics.ListAPIView):
    serializer_class = FlashcardSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Flashcard.objects.filter(subject_id=subject_id).order_by('?')

class AssessmentHistoryView(generics.ListAPIView):
    serializer_class = AssessmentProgressSerializer

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).order_by('-last_attempt')

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile
