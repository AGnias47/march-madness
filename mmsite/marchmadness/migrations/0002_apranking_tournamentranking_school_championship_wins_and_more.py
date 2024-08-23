# Generated by Django 4.2.5 on 2023-09-24 18:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="APRanking",
            fields=[
                ("ranking_id", models.IntegerField(primary_key=True, serialize=False)),
                ("team", models.CharField(max_length=58)),
                ("ranking", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TournamentRanking",
            fields=[
                ("ranking_id", models.IntegerField(primary_key=True, serialize=False)),
                ("team", models.CharField(max_length=58)),
                ("ranking", models.IntegerField()),
                ("conference", models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name="school",
            name="championship_wins",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="school",
            name="final_four_appearances",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="school",
            name="tournament_appearances",
            field=models.IntegerField(default=0),
        ),
    ]
