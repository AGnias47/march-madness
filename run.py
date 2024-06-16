#!/usr/bin/env python

import argparse
import logging
import os

from helpers.random_number_seeding import seed_via_random_api
from models.tournament import MarchMadnessTournament


logging.basicConfig(
    encoding="UTF-8",
    level="INFO",
    handlers=[
        logging.FileHandler("NCAA_Tournament_Results.log"),
        logging.StreamHandler(),
    ],
    format="%(message)s",
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-y",
    "--year",
    type=int,
    default=2024,
    help="Year of tournament; must be 2022 or later",
)
parser.add_argument(
    "-e",
    "--evaluate",
    action="store_true",
    default=False,
    help="Run evaluation mode where user manually selects teams to win",
)
parser.add_argument(
    "-p",
    "--predict",
    help="Runs prediction mode where teams are automatically selected using a "
    "prediction method. One of: ["
    "'random', "
    "'lptr', "
    "'sigmodal', "
    "'ranked', "
    "'ap', "
    "'nickname'"
    "]",
    default=None,
)
parser.add_argument(
    "-a",
    "--ap-rank-weight",
    type=float,
    default=0.75,
    help="Weight for AP rank in weighted predictions",
)
parser.add_argument(
    "-k",
    "--sigmodal-k",
    type=float,
    help="k value; for sigmodal prediction method only",
)
args = parser.parse_args()


if args.evaluate:
    from evaluate.select_team import user_evaluation as prediction_method

    if args.predict:
        raise ValueError("Cannot evaluate and predict at the same time")
elif args.predict:
    if args.predict.casefold() == "random":
        from predict.select_team import random_selection as prediction_method
    elif args.predict.casefold() == "lptr":
        from predict.select_team import (
            weighted_random_selection_lptr as prediction_method,
        )
    elif args.predict.casefold() == "sigmodal":
        from predict.select_team import (
            weighted_random_selection_sigmodal as prediction_method,
        )

        if not args.sigmodal_k:
            pass
    elif args.predict.casefold() == "ranked":
        from predict.select_team import ranked_selection as prediction_method
    elif args.predict.casefold() == "ap":
        from predict.select_team import ap_selection as prediction_method
    elif args.predict.casefold() == "nickname":
        from predict.sentiment_analysis import nickname_sentiment as prediction_method
else:
    from evaluate.select_team import user_evaluation as prediction_method

if random_api_key := os.getenv("RANDOM_API_KEY"):
    seed = seed_via_random_api(0, 10_000, random_api_key)
    print(f"Seeded with {seed}")

tournament = MarchMadnessTournament(
    year=args.year,
    prediction_method=prediction_method,
    prediction_method_kwargs={
        "ap_rank_weight": args.ap_rank_weight,
        "k": args.sigmodal_k,
    },
    log_results=True,
)

tournament.run()
