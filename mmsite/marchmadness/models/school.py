from django.db import models

from .constants import MAX_SCHOOL_LEN
from .game import Game


class School(models.Model):
    name = models.CharField(max_length=MAX_SCHOOL_LEN, primary_key=True, unique=True)
    formal_name = models.CharField(max_length=int(MAX_SCHOOL_LEN * 1.2))
    nickname = models.CharField(max_length=30)
    home_arena = models.CharField(max_length=60, null=True)
    conference = models.CharField(max_length=30)
    tournament_appearances = models.IntegerField(default=0)
    final_four_appearances = models.IntegerField(default=0)
    championship_wins = models.IntegerField(default=0)
    primary_color = models.CharField(max_length=20, null=True)
    secondary_color = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=50, null=True)
    is_private = models.BooleanField(null=False, default=False)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_school"

    def __str__(self):
        return self.name

    def context(self):
        return {
            "name": self.name,
            "formal_name": self.formal_name,
            "nickname": self.nickname,
            "home_arena": self.home_arena,
            "conference": self.conference,
            "tournament_appearances": self.tournament_appearances,
            "final_four_appearances": self.final_four_appearances,
            "championship_wins": self.championship_wins,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "location": self.location,
            "is_private": self.is_private,
        }

    @property
    def list_repr(self):
        r = list()
        r.append(f"Nickname: {self.nickname}")
        r.append(f"Location: {self.location}")
        r.append(f"Colors: {self.primary_color}, {self.secondary_color}")
        is_private_str = "yes" if self.is_private else "no"
        r.append(f"Private: {is_private_str}")
        return r

    def games(self, season):
        return Game.objects.filter(school_name=self.name, season=season).order_by(
            "date"
        )

    def wins(self, season):
        return self.games(season).filter(win=True).count()

    def losses(self, season):
        return self.games(season).filter(win=False).count()

    def record(self, season):
        return f"{self.wins(season)}-{self.losses(season)}"
