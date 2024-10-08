"""
Manages user picks
"""

from django.db import models
from django.dispatch import receiver

from .constants import MAX_SCHOOL_LEN
from .group import Group
from .tournament import Tournament


@receiver(models.signals.pre_save)
def init_groups(sender, instance, **kwargs):
    if instance.pk is None and isinstance(instance, Bracket):
        instance._init_groups()


class Bracket(models.Model):
    year = models.IntegerField()
    season = models.CharField(max_length=9)
    top_left_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="top_left_group"
    )
    bottom_left_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="bottom_left_group"
    )
    top_right_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="top_right_group"
    )
    bottom_right_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="bottom_right_group"
    )
    left_winner = models.CharField(max_length=MAX_SCHOOL_LEN)
    right_winner = models.CharField(max_length=MAX_SCHOOL_LEN)
    champion = models.CharField(max_length=MAX_SCHOOL_LEN)

    class Meta:
        app_label = "marchmadness"
        db_table = f"{app_label}_bracket"

    def _init_groups(self):
        self.season = f"{self.year - 1}-{str(self.year)}"
        self.tournament_info = Tournament.objects.get(year=self.year)
        self.top_left_group = Group.objects.create(
            year=self.year, region=self.tournament_info.top_left_region
        )
        self.bottom_left_group = Group.objects.create(
            year=self.year, region=self.tournament_info.bottom_left_region
        )
        self.top_right_group = Group.objects.create(
            year=self.year, region=self.tournament_info.top_right_region
        )
        self.bottom_right_group = Group.objects.create(
            year=self.year, region=self.tournament_info.bottom_right_region
        )

    @property
    def groups(self):
        return [
            self.top_left_group,
            self.bottom_left_group,
            self.top_right_group,
            self.bottom_right_group,
        ]
