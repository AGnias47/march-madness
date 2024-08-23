"""
Manages user picks
"""

from django.db import models
from .tournament_ranking import TournamentRanking
from .constants import MAX_SCHOOL_LEN


class Group(models.Model):
    year = models.IntegerField()
    region = models.CharField(max_length=30)
    first_four_winner = models.CharField(max_length=MAX_SCHOOL_LEN)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_group"

    @property
    def teams(self):
        return TournamentRanking.objects.filter(year=self.year, region=self.region)

    @property
    def play_in_teams(self):
        return self.teams(play_in=True)

    def team(self, ranking):
        return self.teams.get(ranking=ranking)

    @property
    def play_in_rank(self):
        return self.play_in_teams.first().ranking
