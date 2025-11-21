from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProgressViewSet, QuizAttemptViewSet

router = DefaultRouter()
router.register(r'progress', UserProgressViewSet, basename='progress')
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quiz-attempt')

urlpatterns = router.urls




