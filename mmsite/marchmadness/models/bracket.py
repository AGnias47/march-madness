"""
Manages user picks
"""

from django.db import models
from .tournament import Tournament
from .group import Group


class Bracket(models.Model):
    year = models.IntegerField(primary_key=True, unique=True)
    season = models.CharField(max_length=9)
    left_top_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="left_top_group"
    )
    left_bottom_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="left_bottom_group"
    )
    right_top_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="right_top_group"
    )
    right_bottom_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="right_bottom_group"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.season = f"{self.year-1}-{str(self.year)}"
        self.tournament_info = Tournament.objects.get(year=self.year)
        self.left_top_group = Group.objects.create(
            year=self.year, region=self.tournament_info.left_top_region
        )
        self.left_bottom_group = Group.objects.create(
            year=self.year, region=self.tournament_info.left_bottom_region
        )
        self.right_top_group = Group.objects.create(
            year=self.year, region=self.tournament_info.right_top_region
        )
        self.right_bottom_group = Group.objects.create(
            year=self.year, region=self.tournament_info.right_bottom_region
        )

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_bracket"
