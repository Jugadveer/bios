from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .models import Course, Topic, Lesson, MentorPersona
from .serializers import CourseSerializer, TopicSerializer, LessonSerializer, MentorPersonaSerializer
from .course_views import load_courses_data


# API Viewsets
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def topics(self, request, pk=None):
        course = self.get_object()
        topics = Topic.objects.filter(course=course)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class MentorPersonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MentorPersona.objects.all()
    serializer_class = MentorPersonaSerializer


# Page Views - Default course page redirects to first course
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def course_home(request):
    """Course home page - redirects to first course"""
    courses = load_courses_data()
    if courses and len(courses) > 0:
        first_course = courses[0]
        if isinstance(first_course, dict) and first_course.get("id"):
            return redirect(f'/course/{first_course["id"]}/')
    return render(request, 'courses/course_detail.html', {'course_id': None, 'user': request.user})


@login_required(login_url='/')
def course_detail(request, course_id=None):
    """Course detail page - serves JSON-based course detail"""
    if not course_id:
        courses = load_courses_data()
        if courses and len(courses) > 0:
            course_id = courses[0]["id"]
            return redirect(f'/course/{course_id}/')
    
    return render(request, 'courses/course_detail.html', {
        'course_id': course_id,
        'user': request.user
    })


# Auth views
def login_view(request):
    from django.contrib.auth import authenticate, login
    from django.http import JsonResponse
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/'})
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def signup_view(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import login, authenticate
    from django.http import JsonResponse
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not username or len(username) < 3:
            return JsonResponse({'success': False, 'error': 'Username must be at least 3 characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
        
        if password != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'}, status=400)
        
        if not password or len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/'})
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def logout_view(request):
    from django.contrib.auth import logout
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return redirect('/')
