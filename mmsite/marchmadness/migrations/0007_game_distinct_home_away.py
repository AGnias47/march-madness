# Generated by Django 4.2.5 on 2023-09-24 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0006_remove_game_game_id_remove_rivalry_rivalry_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="distinct_home_away",
            field=models.BooleanField(default=False),
        ),
    ]
