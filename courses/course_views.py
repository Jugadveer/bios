"""
Course views for serving courses from financial_course.json
"""
import json
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Try both possible file names
COURSES_JSON_PATH = None
for filename in ['financial_course.json', 'financial_courses.json']:
    path = os.path.join(settings.BASE_DIR, filename)
    if os.path.exists(path):
        COURSES_JSON_PATH = path
        break

if not COURSES_JSON_PATH:
    COURSES_JSON_PATH = os.path.join(settings.BASE_DIR, 'financial_course.json')


def transform_topic_to_course(topic):
    """Transform a topic (from topics structure) to course format"""
    lessons = topic.get('lessons', [])
    
    # Transform lessons to modules
    modules = []
    for lesson in lessons:
        # Extract Q&A from messages if available
        fixed_qna = []
        messages = lesson.get('messages', [])
        
        # Try to extract Q&A pairs from messages
        # Look for patterns like "Q:" and "A:" or question-answer pairs
        for i, msg in enumerate(messages):
            text = msg.get('text', '')
            sender = msg.get('sender', '')
            
            # If message contains Q&A pattern
            if 'Q:' in text or '?' in text:
                # Try to find answer in next message
                if i + 1 < len(messages):
                    answer_text = messages[i + 1].get('text', '')
                    if answer_text:
                        fixed_qna.append({
                            'q': text.replace('Q:', '').strip(),
                            'a': answer_text.replace('A:', '').strip()
                        })
        
        module = {
            'id': lesson.get('id', ''),
            'title': lesson.get('title', ''),
            'summary': lesson.get('title', ''),  # Use title as summary if no summary field
            'fixed_qna': fixed_qna if isinstance(fixed_qna, list) and len(fixed_qna) > 0 else []
        }
        modules.append(module)
    
    # Calculate duration estimate (5 mins per lesson)
    duration_mins = len(lessons) * 5
    
    course = {
        'id': topic.get('id', ''),
        'title': topic.get('title', ''),
        'overview': topic.get('summary', topic.get('title', '')),
        'duration_mins': duration_mins,
        'source': '',  # Will be extracted from lessons if available
        'modules': modules
    }
    
    return course


def load_courses_data():
    """Load courses from JSON file - use as-is, no transformation"""
    if not COURSES_JSON_PATH or not os.path.exists(COURSES_JSON_PATH):
        print(f"Courses JSON file not found at: {COURSES_JSON_PATH}")
        return []
    
    try:
        with open(COURSES_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                # Direct array of courses (expected format)
                print(f"Loaded {len(data)} courses from {COURSES_JSON_PATH}")
                return data
            elif isinstance(data, dict):
                # Object with 'topics' or 'courses' key
                if 'topics' in data and isinstance(data['topics'], list):
                    # Transform topics to courses format
                    topics = data['topics']
                    courses = [transform_topic_to_course(topic) for topic in topics]
                    print(f"Loaded {len(courses)} courses from {COURSES_JSON_PATH} (transformed from topics)")
                    return courses
                elif 'courses' in data and isinstance(data['courses'], list):
                    print(f"Loaded {len(data['courses'])} courses from {COURSES_JSON_PATH}")
                    return data['courses']
                else:
                    print(f"JSON structure not recognized. Keys: {list(data.keys())}")
                    return []
            else:
                print(f"Unexpected JSON structure: {type(data)}")
                return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []
    except Exception as e:
        print(f"Error loading courses: {e}")
        import traceback
        traceback.print_exc()
        return []


@api_view(['GET'])
@permission_classes([AllowAny])
def get_courses(request):
    """Get all courses from JSON"""
    courses = load_courses_data()
    
    # Ensure we return an array
    if not isinstance(courses, list):
        courses = []
    
    return Response(courses)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_course_detail(request, course_id):
    """Get a specific course by ID"""
    courses = load_courses_data()
    
    # Ensure courses is a list
    if not isinstance(courses, list):
        return Response({"error": "Courses data is not in the expected format"}, status=500)
    
    if not courses:
        return Response({"error": "No courses available"}, status=404)
    
    # Find course by ID (case-insensitive match)
    course = None
    for c in courses:
        if isinstance(c, dict):
            course_id_val = c.get("id", "")
            # Try exact match first
            if course_id_val == course_id:
                course = c
                break
            # Try case-insensitive match
            if course_id_val.lower() == course_id.lower():
                course = c
                break
    
    if not course:
        # Return first course as fallback
        print(f"Course '{course_id}' not found, returning first course")
        course = courses[0] if isinstance(courses[0], dict) else None
        if not course:
            return Response({"error": f"Course '{course_id}' not found"}, status=404)
    
    return Response(course)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_module_detail(request, course_id, module_id):
    """Get a specific module from a course"""
    courses = load_courses_data()
    course = next((c for c in courses if c.get("id") == course_id), None)
    
    if not course:
        return Response({"error": "Course not found"}, status=404)
    
    module = next((m for m in course.get("modules", []) if m.get("id") == module_id), None)
    
    if not module:
        return Response({"error": "Module not found"}, status=404)
    
    return Response({
        "course": {
            "id": course.get("id"),
            "title": course.get("title"),
            "source": course.get("source")
        },
        "module": module
    })

