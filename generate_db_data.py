#!/usr/bin/env python

import argparse
import datetime
import importlib
import logging
from math import isnan
import os

from bs4 import BeautifulSoup

from data.games import get_regular_season_games
from data.schools import (
    get_all_d1_schools,
    add_names_to_schools,
    add_location_and_is_private_to_dataframe,
    add_team_colors_to_dataframe,
)
from helpers.sessions import limiting_retrying_session

# Django setup to use models
import sys

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django  # noqa: E402

django.setup()

from marchmadness.models import (  # noqa: E402
    School,
    Game,
    APRanking,
    TournamentRanking,
    Tournament,
)

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


def parse_score(score):
    score_split = score.split("-")
    return int(score_split[0]), int(score_split[1])


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


def add_games(year):
    previous_year = year - 1
    games_dict = get_regular_season_games(SESSION, year)
    for school, games in games_dict.items():
        for game in games:
            try:
                home_score, away_score = parse_score(game["score"])
            except ValueError:
                continue
            defaults = {
                "season": f"{previous_year}-{year}",
                "home_game": game["home_game"],
                "win": game["win"],
            }
            unique_fields = {
                "date": game["game_date"],
                "school_name": school,
                "opponent": game["opponent"],
                "school_score": home_score,
                "opponent_score": away_score,
            }
            Game.objects.update_or_create(defaults=defaults, **unique_fields)


def add_ap_ranking(year):
    data = SESSION.get(AP_RANKINGS).content
    ap_ranks = BeautifulSoup(data, "html.parser")
    for d in ap_ranks.find("table").find_all("tr")[1:]:
        td = d.find_all("td")
        name = td[1].string.split("(")[0].strip()
        ap_replacement_dict = {"San Diego State": "SDSU"}
        if name in ap_replacement_dict:
            name = ap_replacement_dict[name]
        ranking = int(td[0].string)
        defaults = {"ranking": ranking}
        unique_fields = {"school_name": name, "year": year}
        APRanking.objects.update_or_create(defaults=defaults, **unique_fields)


def add_tournament_rankings_helper(data, conference_name, year):
    play_in_rank = data.pop("play_in_rank")
    for rank, school_name in data.items():
        play_in = False
        if rank == play_in_rank or rank == "play_in":
            play_in = True
            rank = play_in_rank
        defaults = {
            "ranking": rank,
            "region": conference_name,
            "play_in": play_in,
        }
        unique_fields = {
            "school_name": school_name,
            "year": year,
        }
        TournamentRanking.objects.update_or_create(defaults=defaults, **unique_fields)


def add_tournament_rankings(year):
    try:
        ranking_year = importlib.import_module(f"tournament_rankings.r{year}")
    except ModuleNotFoundError:
        logging.error(f"No tournament rankings found for year {year}")
        raise
    add_tournament_rankings_helper(ranking_year.west, WEST, year)
    add_tournament_rankings_helper(ranking_year.east, EAST, year)
    add_tournament_rankings_helper(ranking_year.south, MIDWEST, year)
    add_tournament_rankings_helper(ranking_year.midwest, SOUTH, year)


def add_tournament_info(year):
    try:
        ranking_year = importlib.import_module(f"tournament_rankings.r{year}")
    except ModuleNotFoundError:
        logging.error(f"No tournament rankings found for year {year}")
        raise
    defaults = {
        "left_top_region": ranking_year.region_location["left_top_region"],
        "left_bottom_region": ranking_year.region_location["left_bottom_region"],
        "right_top_region": ranking_year.region_location["right_top_region"],
        "right_bottom_region": ranking_year.region_location["right_bottom_region"],
    }
    unique_fields = {"year": year}
    Tournament.objects.update_or_create(defaults=defaults, **unique_fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--schools",
        action="store_true",
        default=False,
        help="If set, will add schools data to database",
    )
    parser.add_argument(
        "-g",
        "--games",
        action="store_true",
        default=False,
        help="Add games data for the provided year",
    )
    parser.add_argument(
        "-a",
        "--ap-rankings",
        action="store_true",
        default=False,
        help="Add AP rankings; can only be done for the current year",
    )
    parser.add_argument(
        "-t",
        "--tournament-rankings",
        action="store_true",
        help="Add tournament rankings",
    )
    parser.add_argument(
        "-i",
        "--tournament-info",
        action="store_true",
        help="Add tournament info",
    )
    parser.add_argument("-y", "--year", type=int, required=True)
    args = parser.parse_args()
    if args.schools:
        logging.info("Adding schools data")
        add_schools()
    if args.games:
        add_games(args.year)
    if args.ap_rankings:
        if args.year == datetime.datetime.now().year:
            add_ap_ranking(args.year)
        else:
            logging.warning("Unable to add AP rankings for previous years")
    if args.tournament_rankings:
        add_tournament_rankings(args.year)
    if args.tournament_info:
        add_tournament_info(args.year)
