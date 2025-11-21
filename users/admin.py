from django.contrib import admin
from .models import UserProgress, QuizAttempt


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'lesson', 'status', 'progress_percent', 'last_accessed']
    list_filter = ['status', 'course', 'last_accessed']
    search_fields = ['user__username', 'course__title']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'score', 'max_score', 'completed_at']
    list_filter = ['completed_at', 'lesson']
    search_fields = ['user__username']
