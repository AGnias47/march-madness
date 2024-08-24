from django.db import models


class Tournament(models.Model):
    year = models.IntegerField(primary_key=True, unique=True)
    top_left_region = models.CharField(max_length=30)
    bottom_left_region = models.CharField(max_length=30)
    top_right_region = models.CharField(max_length=30)
    bottom_right_region = models.CharField(max_length=30)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_tournament"
