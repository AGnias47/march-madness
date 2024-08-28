#!/usr/bin/env python

"""
Adds data related to a specific tournament year.
"""

import argparse
import datetime
import importlib
import logging
import os

# Django setup to use models
import sys

from bs4 import BeautifulSoup

from data.games import get_regular_season_games
from helpers.sessions import limiting_retrying_session

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django  # noqa: E402

django.setup()

from marchmadness.models.ap_ranking import APRanking  # noqa: E402
from marchmadness.models.game import Game  # noqa: E402
from marchmadness.models.tournament import Tournament  # noqa: E402
from marchmadness.models.tournament_ranking import TournamentRanking  # noqa: E402

# Constants
CURRENT_YEAR = datetime.datetime.now().year
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


def parse_score(score):
    score_split = score.split("-")
    return int(score_split[0]), int(score_split[1])


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
    schools_to_add = list()
    for d in ap_ranks.find("table").find_all("tr")[1:]:
        td = d.find_all("td")
        name = td[1].string.split("(")[0].strip()
        ap_replacement_dict = {"San Diego State": "SDSU"}
        if name in ap_replacement_dict:
            name = ap_replacement_dict[name]
        ranking = int(td[0].string)
        school = APRanking(school_name=name, ranking=ranking, year=year)
        schools_to_add.append(school)
    APRanking.objects.all().delete()
    APRanking.objects.bulk_create(schools_to_add)


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
    add_tournament_rankings_helper(ranking_year.south, SOUTH, year)
    add_tournament_rankings_helper(ranking_year.midwest, MIDWEST, year)


def add_tournament_info(year):
    try:
        ranking_year = importlib.import_module(f"tournament_rankings.r{year}")
    except ModuleNotFoundError:
        logging.error(f"No tournament rankings found for year {year}")
        raise
    defaults = {
        "top_left_region": ranking_year.region_location["top_left_region"],
        "bottom_left_region": ranking_year.region_location["bottom_left_region"],
        "top_right_region": ranking_year.region_location["top_right_region"],
        "bottom_right_region": ranking_year.region_location["bottom_right_region"],
    }
    unique_fields = {"year": year}
    Tournament.objects.update_or_create(defaults=defaults, **unique_fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", "-y", type=int, default=CURRENT_YEAR)
    parser.add_argument(
        "--no-games", "-e", action="store_true", default="False", help="Don't add games"
    )
    args = parser.parse_args()
    year = args.year
    logging.info(f"Adding tournament info for {year}")
    if args.no_games:
        logging.info("Not adding games")
    else:
        logging.info("Adding games")
        add_games(year)
    if year == CURRENT_YEAR:
        logging.info("Adding AP rankings")
        add_ap_ranking(year)
    else:
        logging.warning("Unable to add AP rankings for previous years")
    logging.info("Adding tournament rankings")
    add_tournament_rankings(year)
    logging.info("Adding tournament info")
    add_tournament_info(year)
