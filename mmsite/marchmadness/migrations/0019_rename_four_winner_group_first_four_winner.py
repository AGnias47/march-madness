# Generated by Django 4.2.6 on 2024-08-30 15:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0018_rename_first_four_winner_group_four_winner_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="group",
            old_name="four_winner",
            new_name="first_four_winner",
        ),
    ]
