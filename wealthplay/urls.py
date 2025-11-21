from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),  # Course pages (includes auth routes)
    path('scenario/', include('simulator.urls')),  # Scenario pages
    path('api/courses/', include('courses.urls')),  # API endpoints
    path('api/chat/', include('chat.urls')),
    path('api/users/', include('users.urls')),
    path('api/uploads/', include('uploads.urls')),
    path('api/cursor/', include('cursor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
