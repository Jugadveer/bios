from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, TopicViewSet, LessonViewSet, MentorPersonaViewSet,
    course_home, course_detail, login_view, signup_view, logout_view
)
from .course_views import get_courses, get_course_detail, get_module_detail

# API routes (for /api/courses/)
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'mentors', MentorPersonaViewSet, basename='mentor')

urlpatterns = [
    # JSON-based course API routes (MUST come before router to avoid conflicts)
    path('json/', get_courses, name='get_courses_json'),
    path('json/<str:course_id>/', get_course_detail, name='get_course_json'),
    path('json/<str:course_id>/<str:module_id>/', get_module_detail, name='get_module_json'),
    
    # Auth routes
    path('auth/login/', login_view, name='login'),
    path('auth/signup/', signup_view, name='signup'),
    path('auth/logout/', logout_view, name='logout'),
    
    # Page routes (for /course/)
    path('', course_home, name='course_home'),
    path('<str:course_id>/', course_detail, name='course_detail'),  # Changed to str for JSON course IDs
    
    # API routes (for /api/courses/) - DRF router (comes last)
    path('', include(router.urls)),
]


