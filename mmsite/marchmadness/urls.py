from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("school/", views.select_school, name="select_school"),
    path("school/<str:school_name>", views.school_details, name="school_details"),
]
