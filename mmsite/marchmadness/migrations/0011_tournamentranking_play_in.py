# Generated by Django 4.2.5 on 2023-09-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0010_rename_team_apranking_school_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournamentranking",
            name="play_in",
            field=models.BooleanField(default=False),
        ),
    ]