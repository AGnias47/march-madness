from django.shortcuts import get_object_or_404, render

from .models import TournamentRanking
from .models.school import School
from .models.bracket import Bracket
from .helpers import get_first_four_teams, get_teams_from_rankings


GAMES = [
    ("top_left", "First Four", "first_four"),
    ("bottom_left", "First Four", "first_four"),
    ("top_right", "First Four", "first_four"),
    ("bottom_right", "First Four", "first_four"),
    ("top_left", "First Round", "1_16"),
    ("top_left", "First Round", "2_15"),
    ("top_left", "First Round", "3_14"),
    ("top_left", "First Round", "4_13"),
    ("top_left", "First Round", "5_12"),
    ("top_left", "First Round", "6_11"),
    ("top_left", "First Round", "7_10"),
    ("top_left", "First Round", "8_9"),
    ("bottom_left", "First Round", "1_16"),
    ("bottom_left", "First Round", "2_15"),
    ("bottom_left", "First Round", "3_14"),
    ("bottom_left", "First Round", "4_13"),
    ("bottom_left", "First Round", "5_12"),
    ("bottom_left", "First Round", "6_11"),
    ("bottom_left", "First Round", "7_10"),
    ("bottom_left", "First Round", "8_9"),
    ("top_right", "First Round", "1_16"),
    ("top_right", "First Round", "2_15"),
    ("top_right", "First Round", "3_14"),
    ("top_right", "First Round", "4_13"),
    ("top_right", "First Round", "5_12"),
    ("top_right", "First Round", "6_11"),
    ("top_right", "First Round", "7_10"),
    ("top_right", "First Round", "8_9"),
    ("bottom_right", "First Round", "1_16"),
    ("bottom_right", "First Round", "2_15"),
    ("bottom_right", "First Round", "3_14"),
    ("bottom_right", "First Round", "4_13"),
    ("bottom_right", "First Round", "5_12"),
    ("bottom_right", "First Round", "6_11"),
    ("bottom_right", "First Round", "7_10"),
    ("bottom_right", "First Round", "8_9"),
    ("top_left", "Second Round", "1_8"),
    ("top_left", "Second Round", "2_7"),
    ("top_left", "Second Round", "3_6"),
    ("top_left", "Second Round", "4_5"),
    ("bottom_left", "Second Round", "1_8"),
    ("bottom_left", "Second Round", "2_7"),
    ("bottom_left", "Second Round", "3_6"),
    ("bottom_left", "Second Round", "4_5"),
    ("top_right", "Second Round", "1_8"),
    ("top_right", "Second Round", "2_7"),
    ("top_right", "Second Round", "3_6"),
    ("top_right", "Second Round", "4_5"),
    ("bottom_right", "Second Round", "1_8"),
    ("bottom_right", "Second Round", "2_7"),
    ("bottom_right", "Second Round", "3_6"),
    ("bottom_right", "Second Round", "4_5"),
    ("top_left", "Sweet Sixteen", "1_4"),
    ("top_left", "Sweet Sixteen", "2_3"),
    ("bottom_left", "Sweet Sixteen", "1_4"),
    ("bottom_left", "Sweet Sixteen", "2_3"),
    ("top_right", "Sweet Sixteen", "1_4"),
    ("top_right", "Sweet Sixteen", "2_3"),
    ("bottom_right", "Sweet Sixteen", "1_4"),
    ("bottom_right", "Sweet Sixteen", "2_3"),
    ("top_left", "Elite Eight", "1_2"),
    ("bottom_left", "Elite Eight", "1_2"),
    ("top_right", "Elite Eight", "1_2"),
    ("bottom_right", "Elite Eight", "1_2"),
    ("final_four", "Final Four", "ff_left"),
    ("final_four", "Final Four", "ff_right"),
    ("championship", "National Championship", "championship"),
]


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


def initialize_bracket(request, year):
    bracket = Bracket.objects.create(year=year)
    bracket.save()
    return evaluate(request, bracket.id, 0)


def evaluate(request, bracket_id, game_id):
    if request.method in {"GET", "POST"}:
        bracket = Bracket.objects.get(id=bracket_id)
        bracket.save()
        game = GAMES[game_id]
        region = game[0]
        tournament_round = game[1]
        matchup = game[2]
        try:
            group = getattr(bracket, f"{region}_group")
            region_name = group.region
        except AttributeError:  # None for Final Four and Championship
            group = None
            region_name = None
        if tournament_round == "First Four":
            team_1, team_2 = get_first_four_teams(group)
        elif tournament_round == "First Round":
            team_1_rank, team_2_rank = int(matchup.split("_")[0]), int(
                matchup.split("_")[1]
            )
            team_1, team_2 = get_teams_from_rankings(group, team_1_rank, team_2_rank)
        elif tournament_round in {"Second Round", "Sweet Sixteen", "Elite Eight"}:
            if matchup == "1_8":
                team_1_name = group.w_1_16
                team_2_name = group.w_8_9
            elif matchup == "2_7":
                team_1_name = group.w_2_15
                team_2_name = group.w_7_10
            elif matchup == "3_6":
                team_1_name = group.w_3_14
                team_2_name = group.w_6_11
            elif matchup == "4_5":
                team_1_name = group.w_4_13
                team_2_name = group.w_5_12
            elif matchup == "1_4":
                team_1_name = group.w_1_8
                team_2_name = group.w_4_5
            elif matchup == "2_3":
                team_1_name = group.w_2_7
                team_2_name = group.w_3_6
            elif matchup == "1_2":
                team_1_name = group.w_1_4
                team_2_name = group.w_2_3
            else:
                raise ValueError("Invalid Matchup")
            team_1 = School.objects.get(name=team_1_name)
            team_2 = School.objects.get(name=team_2_name)
        elif matchup == "ff_left":
            team_1 = School.objects.get(name=bracket.top_left_group.winner)
            team_2 = School.objects.get(name=bracket.bottom_left_group.winner)
        elif matchup == "ff_right":
            team_1 = School.objects.get(name=bracket.top_right_group.winner)
            team_2 = School.objects.get(name=bracket.bottom_right_group.winner)
        elif matchup == "championship":
            team_1 = School.objects.get(name=bracket.left_winner)
            team_2 = School.objects.get(name=bracket.right_winner)
        else:
            raise ValueError("Invalid matchup")
        return render(
            request,
            "marchmadness/evaluate.html",
            {
                "season": bracket.season,
                "round": tournament_round,
                "matchup": matchup,
                "team_1": team_1,
                "team_1_rank": TournamentRanking.objects.get(
                    school_name=team_1.name, year=bracket.year
                ).ranking,
                "team_1_record": team_1.record(bracket.season),
                "team_1_games": team_1.games(bracket.season),
                "team_2": team_2,
                "team_2_rank": TournamentRanking.objects.get(
                    school_name=team_2.name, year=bracket.year
                ).ranking,
                "team_2_record": team_2.record(bracket.season),
                "team_2_games": team_2.games(bracket.season),
                "region": "top_left",
                "region_name": region_name,
                "bracket": bracket,
                "game_id": game_id,
            },
        )


def select_winner(request, bracket_id, game_id, winning_team):
    if request.method == "POST":
        bracket = Bracket.objects.get(id=bracket_id)
        region = GAMES[game_id][0]
        try:
            group = getattr(bracket, f"{region}_group")
        except AttributeError:  # None for Final Four and Championship
            group = None
        matchup = GAMES[game_id][2]
        if matchup == "first_four":
            setattr(group, "first_four_winner", winning_team)
        elif matchup == "1_2":
            setattr(group, "winner", winning_team)
        elif matchup == "ff_left":
            bracket.left_winner = winning_team
        elif matchup == "ff_right":
            bracket.right_winner = winning_team
        elif matchup == "championship":
            bracket.champion = winning_team
        else:
            setattr(group, f"w_{matchup}", winning_team)
        if group:
            group.save()
        bracket.save()
        if matchup == "championship":
            return render(
                request,
                "marchmadness/bracket.html",
                {
                    "bracket": bracket,
                },
            )
        return evaluate(request, bracket.id, game_id + 1)


def predict(request, season=None):
    return render(request, "marchmadness/predict.html", {"season": season})
