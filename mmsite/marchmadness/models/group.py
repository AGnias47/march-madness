"""
Manages user picks
"""

from django.db import models
from .tournament_ranking import TournamentRanking
from .constants import MAX_SCHOOL_LEN


class Group(models.Model):
    year = models.IntegerField()
    region = models.CharField(max_length=30)
    # Store first four winner
    first_four_winner = models.CharField(max_length=MAX_SCHOOL_LEN)
    # Store First Round winners
    w_first_1_16 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_2_15 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_3_14 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_4_13 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_5_12 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_6_11 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_7_10 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_first_8_9 = models.CharField(max_length=MAX_SCHOOL_LEN)
    # Store Second Round winners
    w_second_1_8 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_second_2_7 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_second_3_6 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_second_4_5 = models.CharField(max_length=MAX_SCHOOL_LEN)
    # Store Sweet Sixteen winners
    w_sweet_1_4 = models.CharField(max_length=MAX_SCHOOL_LEN)
    w_sweet_2_3 = models.CharField(max_length=MAX_SCHOOL_LEN)
    # Store Elite Eight Group Winner
    winner = models.CharField(max_length=MAX_SCHOOL_LEN)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_group"

    @property
    def teams(self):
        return TournamentRanking.objects.filter(year=self.year, region=self.region)

    @property
    def play_in_teams(self):
        return self.teams.filter(play_in=True)

    def team(self, ranking):
        return self.teams.get(ranking=ranking)

    @property
    def play_in_rank(self):
        return self.play_in_teams.first().ranking
