# Generated by Django 4.2.5 on 2023-09-24 19:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0004_alter_school_home_arena_alter_school_location_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="apranking",
            name="year",
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tournamentranking",
            name="year",
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
