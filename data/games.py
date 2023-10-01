import logging

from bs4 import BeautifulSoup
import dateutil.parser
from dateutil.relativedelta import relativedelta
from requests.adapters import HTTPAdapter, Retry
from requests_ratelimiter import LimiterSession
from tqdm import tqdm

from data.espn import get_teams_from_api, get_name

session = LimiterSession(per_second=1)
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retry))
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) "
        "Gecko/20100101 Firefox/115.0"
    }
)

logger = logging.getLogger(__name__)


def get_regular_season_games(season_year=2023):
    teams = get_teams_from_api(session)
    games = dict()
    for team in tqdm(teams):
        team_name = get_name(team["shortDisplayName"])
        logger.info("Parsing games data for %s", team_name)
        team_games = list()
        schedule_link = next(filter(lambda x: x["text"] == "Schedule", team["links"]))[
            "href"
        ]
        link_with_year = f"{schedule_link}/season/{season_year}"
        schedule_soup = BeautifulSoup(
            session.get(link_with_year).text, features="html.parser"
        )
        schedule_table = schedule_soup.find("tbody", {"class", "Table__TBODY"})
        try:
            rows = [r for r in schedule_table.find_all("tr", {"class": "Table__TR"})]
        except AttributeError:
            logger.warning("No games found for %s", team_name)
            continue
        regular_season_index = [
            idx for idx, s in enumerate(rows) if s.text == "Regular Season"
        ][0]
        rows = rows[regular_season_index + 2 :]
        for row in rows:
            row = [r for r in row]
            day_and_month = row[0].text.strip()
            game_date = dateutil.parser.parse(f"{day_and_month}, {season_year}").date()
            if game_date.month > 4:
                game_date -= relativedelta(years=1)
            opponent = (
                row[1]
                .text.lstrip("0123456789")
                .replace("vs ", "")
                .replace("*", "")
                .replace("@", "")
                .strip()
            )
            score = row[2].text.strip()
            if score[0] == "W":
                win = True
                score = score[1:]
            elif score[0] == "L":
                win = False
                score = score[1:]
            elif score == "Canceled":
                win = None
            elif score == "Postponed":
                win = None
            elif "T" in score:
                win = None
            else:
                raise ValueError("Invalid win-loss character detected: %s", score[0])
            team_games.append(
                {
                    "game_date": game_date,
                    "opponent": get_name(opponent),
                    "score": score,
                    "home_game": "vs" in row[1].text,
                    "win": win,
                }
            )
        games[team_name] = team_games
    return games
