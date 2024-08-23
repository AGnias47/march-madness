"""
Manages user picks
"""

from django.db import models
from .tournament import Tournament
from .group import Group


class Bracket(models.Model):
    year = models.IntegerField(primary_key=True, unique=True)
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
        self.left_top_group = Group.objects.create(year=self.year, region="left_top")
        self.left_bottom_group = Group.objects.create(
            year=self.year, region="left_bottom"
        )
        self.right_top_group = Group.objects.create(year=self.year, region="right_top")
        self.right_bottom_group = Group.objects.create(
            year=self.year, region="right_bottom"
        )

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_bracket"

    @property
    def tournament_info(self):
        return Tournament.objects.get(year=self.year).first()
