from django.db import models

from .constants import MAX_SCHOOL_LEN


class APRanking(models.Model):
    school_name = models.CharField(max_length=MAX_SCHOOL_LEN)
    ranking = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_ap_ranking"
        unique_together = (("school_name", "year"), ("ranking", "year"))

    def __str__(self):
        return f"{self.school_name}: {self.ranking}"
