from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("school/<str:school_name>", views.school, name="school"),
]
