# Generated by Django 4.2.5 on 2023-09-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0014_tournament"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tournament",
            name="id",
        ),
        migrations.AlterField(
            model_name="school",
            name="name",
            field=models.CharField(
                max_length=58, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="year",
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="apranking",
            unique_together={("school_name", "year"), ("ranking", "year")},
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together={
                ("date", "school_name", "opponent", "school_score", "opponent_score")
            },
        ),
        migrations.AlterUniqueTogether(
            name="rivalry",
            unique_together={("team1", "team2")},
        ),
        migrations.AlterUniqueTogether(
            name="tournamentranking",
            unique_together={("school_name", "year")},
        ),
    ]
