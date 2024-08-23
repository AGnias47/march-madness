from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("school/", views.school, name="school"),
    path("school/<str:school_name>", views.school_details, name="school_details"),
    path(
        "school/<str:school_name>/games/<str:season>",
        views.school_games,
        name="school_games",
    ),
    path("evaluate/", views.evaluate, name="evaluate"),
    path(
        "evaluate/<int:year>/<str:region>/<str:tournament_round>/<str:matchup>/",
        views.evaluate,
        name="evaluate",
    ),
    path("predict/", views.predict, name="predict"),
    path("predict/random", views.predict, name="predict_random"),
    path("predict/ranked", views.predict, name="predict_ranked"),
    path("predict/ap", views.predict, name="predict_ap"),
    path("predict/lptr", views.predict, name="predict_lptr"),
    path("predict/sigmodal", views.predict, name="predict_sigmodal"),
    path("predict/nickname", views.predict, name="predict_nickname"),
]
