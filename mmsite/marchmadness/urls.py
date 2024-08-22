from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("school/", views.school, name="select_school"),
    path("school/<str:school_name>", views.school_details, name="school_details"),
    path(
        "school/<str:school_name>/games/<str:season>",
        views.school_games,
        name="school_games",
    ),
    path("evaluate/", views.evaluate, name="evaluate"),
    path("predict/", views.predict, name="predict"),
]
