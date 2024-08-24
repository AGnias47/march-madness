from django.shortcuts import get_object_or_404, render
from .models.school import School
from .models.bracket import Bracket


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
    school = get_object_or_404(School, name=school_name)
    return render(
        request,
        "marchmadness/school_games.html",
        {
            "school_name": school_name,
            "games": school.games(season),
            "season": season,
            "record": school.record(season),
        },
    )


def evaluate(request, year, region, tournament_round, matchup, bracket=None):
    if request.method == "GET":
        if not bracket:
            bracket = Bracket(year=year)
            bracket.save()
        else:
            bracket = Bracket.objects.get(id=bracket)
        if tournament_round == "first_four":
            team_1_name = bracket.left_top_group.play_in_teams.first().school_name
            team_1 = School.objects.get(name=team_1_name)
            team_2_name = bracket.left_top_group.play_in_teams.last().school_name
            team_2 = School.objects.get(name=team_2_name)
        return render(
            request,
            "marchmadness/evaluate.html",
            {
                "season": bracket.season,
                "round": tournament_round,
                "matchup": matchup,
                "team_1": team_1,
                "team_1_record": team_1.record(bracket.season),
                "team_1_games": team_1.games(bracket.season),
                "team_2": team_2,
                "team_2_record": team_2.record(bracket.season),
                "team_2_games": team_2.games(bracket.season),
                "region": region,
                "bracket": bracket,
            },
        )
    else:
        pass


def predict(request, season=None):
    return render(request, "marchmadness/predict.html", {"season": season})
