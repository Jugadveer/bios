from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class MentorPersona(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


# User-specific course customization (for future use)
class UserCourseCustomization(models.Model):
    """Store user-specific customizations for courses (different questions, content, etc.)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_customizations')
    course_id = models.CharField(max_length=100)  # Course ID from JSON
    custom_content = models.JSONField(default=dict, blank=True)  # Store custom Q&A, modules, etc.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course_id']
        indexes = [
            models.Index(fields=['user', 'course_id']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course_id}"


# User-specific course progress tracking for JSON-based courses
class UserCourseProgress(models.Model):
    """Track user progress for JSON-based courses"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='json_course_progress')
    course_id = models.CharField(max_length=100)  # Course ID from JSON
    module_id = models.CharField(max_length=100, blank=True)  # Module ID from JSON
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percent = models.FloatField(default=0.0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course_id', 'module_id']
        indexes = [
            models.Index(fields=['user', 'course_id']),
            models.Index(fields=['user', 'course_id', 'module_id']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course_id} - {self.status}"
