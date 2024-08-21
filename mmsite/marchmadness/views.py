from django.http import HttpResponse
from django.template import loader
from .models import School


def index(request):
    template = loader.get_template("marchmadness/index.html")
    context = {"welcome_message": "Welcome to the March Madness site!"}
    return HttpResponse(template.render(context, request))


def school(request, school_name):
    school_name = school_name.title()
    school = School.objects.filter(name=school_name).first()
    return HttpResponse(school.view())
