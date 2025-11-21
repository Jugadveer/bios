from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Landing page with links to Course and Scenario"""
    return render(request, 'landing.html', {'user': request.user})
