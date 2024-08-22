#!/usr/bin/env python

"""
Adds static and generally non-changing data about D1 basketball
schools to the database. Can be run repeatedly and in a deterministic fashion.
"""

import logging
import os

# Django setup to use models
import sys
from math import isnan

from data.schools import (
    add_location_and_is_private_to_dataframe,
    add_names_to_schools,
    add_team_colors_to_dataframe,
    get_all_d1_schools,
)
from helpers.sessions import limiting_retrying_session

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django  # noqa: E402

django.setup()

from marchmadness.models.school import School  # noqa: E402

# Constants
AP_RANKINGS = "https://www.ncaa.com/rankings/basketball-men/d1/associated-press"
WEST = "West"
EAST = "East"
SOUTH = "South"
MIDWEST = "Midwest"
logging.basicConfig(
    encoding="UTF-8",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
    format="%(message)s",
)
SESSION = limiting_retrying_session()


def get_parens_num(prov_str):
    return int(prov_str.split(")")[0].split("(")[1])


def insert_bool(val):
    if isnan(val):
        return False
    return val


def add_schools():
    logging.info("Getting school data")
    df = get_all_d1_schools()
    logging.info("Adding short names to schools")
    add_names_to_schools(df)
    logging.info("Adding team colors")
    add_team_colors_to_dataframe(SESSION, df)
    logging.info("Adding location and is_private info")
    add_location_and_is_private_to_dataframe(df)
    df = df[~df["Name"].duplicated(keep=False)]
    for i, row in df.iterrows():
        defaults = {
            "formal_name": row["School"],
            "nickname": row["Nickname"],
            "home_arena": row["Home arena"],
            "conference": row["Conference"],
            "tournament_appearances": get_parens_num(row["Tournament appearances"]),
            "final_four_appearances": get_parens_num(row["Final Four appearances"]),
            "championship_wins": get_parens_num(row["Championship wins"]),
            "primary_color": row["Primary Color"],
            "secondary_color": row["Secondary Color"],
            "location": row["Location"],
            "is_private": insert_bool(row["Is Private"]),
        }
        unique_fields = {"name": row["Name"]}
        School.objects.update_or_create(defaults=defaults, **unique_fields)


if __name__ == "__main__":
    logging.info("Adding schools data")
    add_schools()
