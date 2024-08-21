from django.shortcuts import render
from .models import School


def index(request):
    context = {"welcome_message": "Welcome to the March Madness site!"}
    return render(request, "marchmadness/index.html", context)


def school(request, school_name):
    school_name = school_name.title()
    school = School.objects.filter(name=school_name).first()
    return render(request, "marchmadness/school.html", school.context())
