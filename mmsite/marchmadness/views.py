from django.http import HttpResponse
from .models import School


def index(request):
    return HttpResponse("Hello, world. You're at the March Madness index.")


def school(request, school_name):
    school_name = school_name.title()
    school = School.objects.filter(name=school_name).first()
    return HttpResponse(school)
