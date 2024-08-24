from django.shortcuts import get_object_or_404, render
from .models.school import School
from .models.bracket import Bracket
from .helpers import get_first_four_teams, get_teams_from_rankings


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


def evaluate(request, year):
    if request.method in {"GET", "POST"}:
        bracket = Bracket(year=year)
        bracket.save()
        group = bracket.top_left_group
        team_1, team_2 = get_first_four_teams(group)
        return render(
            request,
            "marchmadness/evaluate.html",
            {
                "season": bracket.season,
                "round": "First Four",
                "matchup": "first_four",
                "team_1": team_1,
                "team_1_record": team_1.record(bracket.season),
                "team_1_games": team_1.games(bracket.season),
                "team_2": team_2,
                "team_2_record": team_2.record(bracket.season),
                "team_2_games": team_2.games(bracket.season),
                "region": "top_left",
                "bracket": bracket,
            },
        )


def select_winner(request, bracket_id, region, tournament_round, matchup, winning_team):
    if request.method == "POST":
        bracket = Bracket.objects.get(id=bracket_id)
        if region == "top_left":
            group = bracket.top_left_group
        elif region == "top_right":
            group = bracket.top_right_group
        elif region == "bottom_left":
            group = bracket.bottom_left_group
        elif region == "bottom_right":
            group = bracket.bottom_right_group
        else:
            raise ValueError(f"Invalid region: {region}")
        if matchup == "first_four":
            group.first_four_winner = winning_team
            # Get teams for the first round
            matchup = "1_16"
            team_1, team_2 = get_teams_from_rankings(group, 1, 16)
        elif matchup == "1_16":
            group.w_first_1_16 = winning_team
            matchup = "2_15"
            team_1, team_2 = get_teams_from_rankings(group, 2, 15)
        elif matchup == "2_15":
            group.w_first_2_15 = winning_team
            matchup = "3_14"
            team_1, team_2 = get_teams_from_rankings(group, 3, 14)
        elif matchup == "3_14":
            group.w_first_3_14 = winning_team
            matchup = "4_13"
            team_1, team_2 = get_teams_from_rankings(group, 4, 13)
        elif matchup == "4_13":
            group.w_first_4_13 = winning_team
            matchup = "5_12"
            team_1, team_2 = get_teams_from_rankings(group, 5, 12)
        elif matchup == "5_12":
            group.w_first_5_12 = winning_team
            matchup = "6_11"
            team_1, team_2 = get_teams_from_rankings(group, 6, 11)
        elif matchup == "6_11":
            group.w_first_6_11 = winning_team
            matchup = "7_10"
            team_1, team_2 = get_teams_from_rankings(group, 7, 10)
        elif matchup == "7_10":
            group.w_first_7_10 = winning_team
            matchup = "8_9"
            team_1, team_2 = get_teams_from_rankings(group, 8, 9)
        elif matchup == "8_9":
            group.w_first_8_9 = winning_team
            # If there are still remaining regions in the first round go to them,
            #   else go to the second round
            if region == "top_left":
                region = "bottom_left"
                matchup = "first_four"
                team_1, team_2 = get_first_four_teams(bracket.bottom_left_group)
            elif region == "bottom_left":
                region = "top_right"
                matchup = "first_four"
                team_1, team_2 = get_first_four_teams(bracket.top_right_group)
            elif region == "top_right":
                region = "bottom_right"
                matchup = "first_four"
                team_1, team_2 = get_first_four_teams(bracket.bottom_right_group)
            elif region == "bottom_right":
                region = "top_left"
                group = bracket.top_left_group
                matchup = "1_8"
                team_1 = group.w_first_1_16
                team_2 = group.w_first_8_9
                tournament_round = "Second Round"
        elif matchup == "1_8":
            group.w_second_1_8 = winning_team
            matchup = "2_7"
            team_1 = group.w_first_2_15
            team_2 = group.w_first_7_10
        elif matchup == "2_7":
            group.w_second_2_7 = winning_team
            matchup = "3_6"
            team_1 = group.w_first_3_14
            team_2 = group.w_first_6_11
        elif matchup == "3_6":
            group.w_second_3_6 = winning_team
            matchup = "4_5"
            team_1 = group.w_first_4_13
            team_2 = group.w_first_5_12
        elif matchup == "4_5":
            group.w_second_4_5 = winning_team
            if region == "top_left":
                region = "bottom_left"
                group = bracket.bottom_left_group
                matchup = "1_8"
                team_1 = group.w_first_1_16
                team_2 = group.w_first_8_9
            elif region == "bottom_left":
                region = "top_right"
                group = bracket.top_right_group
                matchup = "1_8"
                team_1 = group.w_first_1_16
                team_2 = group.w_first_8_9
            elif region == "top_right":
                region = "bottom_right"
                group = bracket.bottom_right_group
                matchup = "1_8"
                team_1 = group.w_first_1_16
                team_2 = group.w_first_8_9
            elif region == "bottom_right":
                region = "top_left"
                group = bracket.top_left_group
                matchup = "1_4"
                team_1 = group.w_second_1_8
                team_2 = group.w_second_4_5
                tournament_round = "Sweet Sixteen"
            else:
                raise ValueError(f"Invalid region: {region}")
        elif matchup == "1_4":
            group.w_sweet_1_4 = winning_team
            matchup = "2_3"
            team_1 = group.w_second_2_7
            team_2 = group.w_second_3_6
        elif matchup == "2_3":
            group.w_sweet_2_3 = winning_team
            if region == "top_left":
                region = "bottom_left"
                group = bracket.bottom_left_group
                matchup = "1_4"
                team_1 = group.w_second_1_8
                team_2 = group.w_second_4_5
            elif region == "bottom_left":
                region = "top_right"
                group = bracket.top_right_group
                matchup = "1_4"
                team_1 = group.w_second_1_8
                team_2 = group.w_second_4_5
            elif region == "top_right":
                region = "bottom_right"
                group = bracket.bottom_right_group
                matchup = "1_4"
                team_1 = group.w_second_1_8
                team_2 = group.w_second_4_5
            elif region == "bottom_right":
                region = "top_left"
                group = bracket.top_left_group
                matchup = "1_2"
                team_1 = group.w_sweet_1_4
                team_2 = group.w_sweet_2_3
                tournament_round = "Sweet Sixteen"
            else:
                raise ValueError(f"Invalid region: {region}")
        elif matchup == "1_2":
            group.group_winner = winning_team
            if region == "top_left":
                region = "bottom_left"
                group = bracket.bottom_left_group
                team_1 = group.w_sweet_1_4
                team_2 = group.w_sweet_2_3
            elif region == "bottom_left":
                region = "top_right"
                group = bracket.top_right_group
                team_1 = group.w_sweet_1_4
                team_2 = group.w_sweet_2_3
            elif region == "top_right":
                region = "bottom_right"
                group = bracket.bottom_right_group
                team_1 = group.w_sweet_1_4
                team_2 = group.w_sweet_2_3
            elif region == "bottom_right":
                region = "top_left"
                group = bracket.top_left_group
                matchup = "ff_left"
                team_1 = bracket.top_left_group.winner
                team_2 = bracket.bottom_left_group.winner
                tournament_round = "Final Four"
            else:
                raise ValueError(f"Invalid region: {region}")
        elif matchup == "ff_left":
            bracket.left_winner = winning_team
            matchup = "ff_right"
            team_1 = bracket.top_right_group.winner
            team_2 = bracket.bottom_right_group.winner
        elif matchup == "ff_right":
            bracket.right_winner = winning_team
            matchup = "championship"
            team_1 = bracket.left_winner
            team_2 = bracket.right_winner
        elif matchup == "championship":
            bracket.champion = winning_team
            return render(
                request,
                "marchmadness/bracket.html",
                {
                    "bracket": bracket,
                },
            )
        else:
            raise ValueError(f"Invalid matchup: {matchup}")
        group.save()
        bracket.save()
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


def predict(request, season=None):
    return render(request, "marchmadness/predict.html", {"season": season})
