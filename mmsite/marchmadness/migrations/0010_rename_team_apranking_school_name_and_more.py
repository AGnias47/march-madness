# Generated by Django 4.2.5 on 2023-09-24 22:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0009_remove_apranking_ranking_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apranking",
            old_name="team",
            new_name="school_name",
        ),
        migrations.RenameField(
            model_name="tournamentranking",
            old_name="team",
            new_name="school_name",
        ),
    ]
