from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import UserProgress, QuizAttempt
from .serializers import UserProgressSerializer, QuizAttemptSerializer
from courses.models import Course, Lesson


class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def course_progress(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id required'}, status=status.HTTP_400_BAD_REQUEST)

        progress = UserProgress.objects.filter(user=request.user, course_id=course_id)
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_progress(self, request):
        lesson_id = request.data.get('lesson_id')
        status_value = request.data.get('status', 'in_progress')
        progress_percent = request.data.get('progress_percent', 0.0)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

        progress, created = UserProgress.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            course=lesson.topic.course,
            topic=lesson.topic,
            defaults={
                'status': status_value,
                'progress_percent': progress_percent,
                'last_accessed': timezone.now()
            }
        )

        if created:
            progress.started_at = timezone.now()
            progress.save()

        if status_value == 'completed':
            progress.completed_at = timezone.now()
            progress.save()

        serializer = self.get_serializer(progress)
        return Response(serializer.data)


class QuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson_id')
        quiz_data = request.data.get('quiz_data', {})

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

        # Calculate score (simplified - should match answers from lesson metadata)
        score = 0.0
        max_score = len(quiz_data.get('answers', []))

        attempt = QuizAttempt.objects.create(
            user=request.user,
            lesson=lesson,
            quiz_data=quiz_data,
            score=score,
            max_score=max_score
        )

        serializer = self.get_serializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
