from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='scenario_home'), # Redirects to /scenario/play/1/
    path('play/<int:scenario_id>/', views.scenario_play, name='scenario_play'),
    path('api/save-result/', views.save_scenario_result, name='save_result'),
]