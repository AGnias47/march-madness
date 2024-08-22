from django.db import models

from .ap_ranking import APRanking
from .constants import MAX_SCHOOL_LEN
from .game import Game
from .school import School


class TournamentRanking(models.Model):
    school_name = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()
    region = models.CharField(max_length=30)
    play_in = models.BooleanField(default=False)
    year = models.IntegerField()

    class Meta:
        unique_together = ("school_name", "year")
        app_label = "marchmadness"
        db_table = f"{app_label}_tournamentranking"

    def __str__(self):
        return f"{self.school_name}: {self.ranking} ({self.region})"

    @property
    def games(self):
        season = f"{self.year - 1}-{self.year}"
        return Game.objects.filter(
            school_name=self.school_name, season=season
        ).order_by("-date")

    @property
    def school(self):
        return School.objects.filter(name=self.school_name).first()

    @property
    def school_info(self):
        return self.school.list_repr

    @property
    def nickname(self):
        return self.school.nickname

    @property
    def record(self):
        total_games = self.games.count()
        wins = self.games.filter(win=True).count()
        losses = total_games - wins
        return f"{wins}-{losses}"

    @property
    def ap_ranking(self):
        try:
            return APRanking.objects.get(
                school_name=self.school_name, year=self.year
            ).ranking
        except APRanking.DoesNotExist:
            return None

    def recent_record(self, n):
        wins = 0
        for game in self.games[:10]:
            if game.win:
                wins += 1
        losses = n - wins
        return f"{wins}-{losses}"

    @property
    def tournament_repr(self):
        r = list()
        r.append(f"{self.ranking}. {self.school_name}")
        if self.ap_ranking:
            r.append(f"AP Rank: {self.ap_ranking}")
        try:
            r.append(f"Conference: {self.school.conference}")
        except AttributeError:
            pass
        try:
            r.append(
                f"Record: {self.record}  ({self.recent_record(10)} in last 10 games)"
            )
        except AttributeError:
            pass
        return r

    @property
    def game_results(self):
        results = []
        for game in self.games:
            result = "Win" if game.win else "Loss"
            home_or_away = "vs." if game.home_game else "@"
            results.append(
                f"{result} {game.school_score}-{game.opponent_score} "
                f"{home_or_away} {game.opponent}"
            )
        return results
