from django.db import models


class Tournament(models.Model):
    year = models.IntegerField(primary_key=True, unique=True)
    left_top_region = models.CharField(max_length=30)
    left_bottom_region = models.CharField(max_length=30)
    right_top_region = models.CharField(max_length=30)
    right_bottom_region = models.CharField(max_length=30)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_tournament"
