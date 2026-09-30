from django.shortcuts import render
from .models import Courses
# Create your views here.

def courses_list(request):
    courses = Courses.objects.all()
    return render(request, 'learniva_app/courses_list.html', {'courses': courses})