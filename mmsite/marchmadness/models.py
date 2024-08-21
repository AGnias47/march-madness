from django.db import models

MAX_SCHOOL_LEN = len("North Carolina Agricultural and Technical State University")


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

    def __str__(self):
        return self.name

    def view(self):
        return (
            f"Team: {self.name}\n"
            f"Nickname: {self.nickname}\n"
            f"Location: {self.location}\n"
            f"Colors: {self.primary_color}, {self.secondary_color}\n"
            f"Private: {self.is_private}"
        )

    @property
    def list_repr(self):
        r = list()
        r.append(f"Nickname: {self.nickname}")
        r.append(f"Location: {self.location}")
        r.append(f"Colors: {self.primary_color}, {self.secondary_color}")
        is_private_str = "yes" if self.is_private else "no"
        r.append(f"Private: {is_private_str}")
        return r


class Game(models.Model):
    date = models.DateField()
    season = models.CharField(max_length=9)
    school_name = models.CharField(max_length=MAX_SCHOOL_LEN)
    opponent = models.CharField(max_length=MAX_SCHOOL_LEN)
    school_score = models.IntegerField()
    opponent_score = models.IntegerField()
    home_game = models.BooleanField(default=True)
    win = models.BooleanField(default=False)

    class Meta:
        # See /team/schedule/_/id/140/season/2021 for instance of two teams playing
        #   each other on the same day. Theoretically, there could be an instance where
        #   this unique_together constraint is violated, but it is very unlikely.
        unique_together = (
            "date",
            "school_name",
            "opponent",
            "school_score",
            "opponent_score",
        )

    def __str__(self):
        return (
            f"{self.school_name} vs. {self.opponent} "
            f"({self.date}): {self.school_score}-{self.opponent_score}"
        )

    def point_differential(self):
        return abs(int(self.school_score) - int(self.opponent_score))


class Rivalry(models.Model):
    team1 = models.CharField(max_length=MAX_SCHOOL_LEN)
    team2 = models.CharField(max_length=MAX_SCHOOL_LEN)

    class Meta:
        unique_together = ("team1", "team2")

    def __str__(self):
        return f"{self.team1} vs. {self.team2}"


class APRanking(models.Model):
    school_name = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        unique_together = (("school_name", "year"), ("ranking", "year"))

    def __str__(self):
        return f"{self.school_name}: {self.ranking}"


class TournamentRanking(models.Model):
    school_name = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()
    region = models.CharField(max_length=30)
    play_in = models.BooleanField(default=False)
    year = models.IntegerField()

    class Meta:
        unique_together = ("school_name", "year")

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


class Tournament(models.Model):
    year = models.IntegerField(primary_key=True, unique=True)
    left_top_region = models.CharField(max_length=30)
    left_bottom_region = models.CharField(max_length=30)
    right_top_region = models.CharField(max_length=30)
    right_bottom_region = models.CharField(max_length=30)
