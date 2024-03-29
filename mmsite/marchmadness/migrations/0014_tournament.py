# Generated by Django 4.2.5 on 2023-09-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0013_rename_conference_tournamentranking_region"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField()),
                ("left_top_region", models.CharField(max_length=30)),
                ("left_bottom_region", models.CharField(max_length=30)),
                ("right_top_region", models.CharField(max_length=30)),
                ("right_bottom_region", models.CharField(max_length=30)),
            ],
        ),
    ]
