from django.db import models

MAX_SCHOOL_LEN = len("North Carolina Agricultural and Technical State University")


class School(models.Model):
    name = models.CharField(max_length=MAX_SCHOOL_LEN, primary_key=True)
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

    def __str__(self):
        return self.name


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    season = models.CharField(max_length=9)
    home_team = models.CharField(max_length=MAX_SCHOOL_LEN)
    away_team = models.CharField(max_length=MAX_SCHOOL_LEN)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return (
            f"{self.home_team} vs. {self.away_team} "
            f"({self.date}): {self.home_score}-{self.away_score}"
        )

    def winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.away_score > self.home_score:
            return self.away_team
        else:
            return None

    def point_differential(self):
        return abs(int(self.home_score) - int(self.away_score))


class Rivalry(models.Model):
    rivalry_id = models.IntegerField(primary_key=True)
    team1 = models.CharField(max_length=MAX_SCHOOL_LEN)
    team2 = models.CharField(max_length=MAX_SCHOOL_LEN)

    def __str__(self):
        return f"{self.team1} vs. {self.team2}"


class APRanking(models.Model):
    ranking_id = models.IntegerField(primary_key=True)
    team = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()

    def __str__(self):
        return f"{self.team}: {self.ranking}"


class TournamentRanking(models.Model):
    ranking_id = models.IntegerField(primary_key=True)
    team = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()
    conference = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.team}: {self.ranking} ({self.conference})"
