from rest_framework import serializers
from .models import UserProgress, QuizAttempt
from courses.serializers import CourseSerializer, LessonSerializer


class UserProgressSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'course', 'topic', 'lesson', 'status', 'progress_percent', 'started_at', 'completed_at', 'last_accessed']


class QuizAttemptSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'lesson', 'quiz_data', 'score', 'max_score', 'completed_at']




