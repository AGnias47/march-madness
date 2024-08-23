from django.shortcuts import get_object_or_404, render
from .models.school import School
from .models.game import Game
from .models.bracket import Bracket
from .models.group import Group


def index(request):
    context = {"welcome_message": "Welcome to the March Madness site!"}
    return render(request, "marchmadness/index.html", context)


def school(request):
    schools = School.objects.all()
    schools = sorted(schools, key=lambda x: x.name)
    if selected_school := request.GET.get("school_name"):
        selected_school_obj = School.objects.get(name=selected_school)
    else:
        selected_school_obj = None
    return render(
        request,
        "marchmadness/school.html",
        {
            "schools": schools,
            "selected_school": selected_school_obj,
        },
    )


def school_details(request, school_name):
    school = get_object_or_404(School, name=school_name)
    return render(request, "marchmadness/school_details.html", school.context())


def school_games(request, school_name, season):
    games = Game.objects.filter(school_name=school_name, season=season).order_by("date")
    return render(
        request,
        "marchmadness/school_games.html",
        {
            "school_name": school_name,
            "games": games,
            "season": season,
            "wins": len([game for game in games if game.win]),
            "losses": len([game for game in games if not game.win]),
        },
    )


def evaluate(request, season, region, tournament_round, matchup, bracket=None):
    if not bracket:
        bracket = Bracket(year=season)
    group = Group.objects.get(region=region, year=season)
    if tournament_round == "first_four":
        team_1 = group.play_in_teams.first()
        team_2 = group.play_in_teams.last()
    return render(
        request,
        "marchmadness/evaluate.html",
        {
            "season": season,
            "round": tournament_round,
            "matchup": matchup,
            "team_1": team_1,
            "team_2": team_2,
            "region": region,
            "bracket": bracket,
        },
    )


def predict(request, season=None):
    return render(request, "marchmadness/predict.html", {"season": season})
