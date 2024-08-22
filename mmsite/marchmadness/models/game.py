from django.db import models

from .constants import MAX_SCHOOL_LEN


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
        app_label = "marchmadness"
        db_table = f"{app_label}_game"

    def __str__(self):
        return (
            f"{self.school_name} vs. {self.opponent} "
            f"({self.date}): {self.school_score}-{self.opponent_score}"
        )

    def point_differential(self):
        return abs(int(self.school_score) - int(self.opponent_score))
