from django.shortcuts import get_object_or_404, render, redirect
from .models import School


def index(request):
    context = {"welcome_message": "Welcome to the March Madness site!"}
    return render(request, "marchmadness/index.html", context)


def select_school(request):
    if request.method == "POST":
        selected_school = request.POST.get("school_name")
        return redirect("school_details", school_name=selected_school)
    schools = School.objects.all()
    schools = sorted(schools, key=lambda x: x.name)
    return render(request, "marchmadness/select_school.html", {"schools": schools})


def school_details(request, school_name):
    school = get_object_or_404(School, name=school_name)
    return render(request, "marchmadness/school_details.html", school.context())
