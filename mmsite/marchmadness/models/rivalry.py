from django.db import models

from .constants import MAX_SCHOOL_LEN


class Rivalry(models.Model):
    team1 = models.CharField(max_length=MAX_SCHOOL_LEN)
    team2 = models.CharField(max_length=MAX_SCHOOL_LEN)

    class Meta:
        unique_together = ("team1", "team2")
        app_label = "marchmadness"
        db_table = f"{app_label}_rivalry"

    def __str__(self):
        return f"{self.team1} vs. {self.team2}"
