from django.core.exceptions import MultipleObjectsReturned

from .models.school import School


def get_teams_from_rankings(group, team_1_ranking, team_2_ranking):
    try:
        team_1_name = group.team(team_1_ranking).school_name
        team_1 = School.objects.get(name=team_1_name)
    except MultipleObjectsReturned as e:
        teams_returned = group.teams.filter(ranking=team_1_ranking)
        not_play_in = teams_returned.filter(play_in=False)
        if not_play_in.count() > 0:
            raise e
        team_1 = School.objects.get(name=group.first_four_winner)
    try:
        team_2_name = group.team(team_2_ranking).school_name
        team_2 = School.objects.get(name=team_2_name)
    except MultipleObjectsReturned as e:
        teams_returned = group.teams.filter(ranking=team_2_ranking)
        not_play_in = teams_returned.filter(play_in=False)
        if not_play_in.count() > 0:
            raise e
        team_2 = School.objects.get(name=group.first_four_winner)
    return team_1, team_2


def get_first_four_teams(group):
    team_1_name = group.play_in_teams.first().school_name
    team_1 = School.objects.get(name=team_1_name)
    team_2_name = group.play_in_teams.last().school_name
    team_2 = School.objects.get(name=team_2_name)
    return team_1, team_2
