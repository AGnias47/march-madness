from django.shortcuts import get_object_or_404, render
from .models import School


def index(request):
    context = {"welcome_message": "Welcome to the March Madness site!"}
    return render(request, "marchmadness/index.html", context)


def select_school(request):
    schools = School.objects.all()
    schools = sorted(schools, key=lambda x: x.name)
    if selected_school := request.GET.get("school_name"):
        selected_school_obj = School.objects.get(name=selected_school)
    else:
        selected_school_obj = None
    return render(
        request,
        "marchmadness/select_school.html",
        {
            "schools": schools,
            "selected_school": selected_school_obj,
        },
    )


def school_details(request, school_name):
    school = get_object_or_404(School, name=school_name)
    return render(request, "marchmadness/school_details.html", school.context())
