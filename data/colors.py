"""
Module for gathering and parsing data on school colors
"""

import logging
from enum import Enum
from data.espn import get_teams_from_api, get_name
import webcolors

logger = logging.getLogger(__name__)


class Colors(Enum):
    WHITE = 1
    BLACK = 2
    RED = 3
    BLUE = 4
    GREEN = 5
    YELLOW = 6
    ORANGE = 7
    PURPLE = 8
    BROWN = 9
    GRAY = 10
    NAVY = 11
    TEAL = 12
    LIGHT_BLUE = 13
    GOLD = 14

    def __repr__(self):
        return self.name.lower()

    def __str__(self):
        return self.name.lower()


def get_all_school_colors(session):
    teams = get_teams_from_api(session)
    colors_dict = dict()
    for team in teams:
        team_name = get_name(team["shortDisplayName"])
        if team_name in SCHOOL_COLOR_DICT:
            colors_dict[team_name] = {
                "primary_color": SCHOOL_COLOR_DICT[team_name]["primary_color"],
                "secondary_color": SCHOOL_COLOR_DICT[team_name]["secondary_color"],
            }
        else:
            try:
                colors_dict[team_name] = {
                    "primary_color": get_color_name(team["color"]),
                    "secondary_color": get_color_name(team.get("alternateColor")),
                }
            except KeyError:
                logger.warning(f"[warning] Could not find colors for {team_name}")
    return colors_dict


def closest_colour(requested_hex):
    """
    Converts a hex color to a readable name

    References
    ----------
    https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python

    Parameters
    ----------
    requested_hex: str

    Returns
    -------

    """
    min_colours = {}
    requested_rgb = webcolors.hex_to_rgb(f"#{requested_hex}")
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_rgb[0]) ** 2
        gd = (g_c - requested_rgb[1]) ** 2
        bd = (b_c - requested_rgb[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_color_name(hex_color):
    """
    Gets a color name from a hex color value, then further simplifies it using
    COLOR_DICT

    Parameters
    ----------
    hex_color: str

    Returns
    -------
    str
    """
    if not hex_color:
        return None
    try:
        color = webcolors.hex_to_name(hex_color)
    except ValueError:
        color = closest_colour(hex_color)
    try:
        return COLOR_DICT[color]
    except KeyError:
        raise ValueError(f"Color {color} not found in COLOR_DICT")


SCHOOL_COLOR_DICT = {
    "Alabama": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Arizona": {"primary_color": Colors.RED, "secondary_color": Colors.BLUE},
    "Arizona State": {"primary_color": Colors.RED, "secondary_color": Colors.GOLD},
    "Arkansas": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Auburn": {"primary_color": Colors.NAVY, "secondary_color": Colors.ORANGE},
    "Baylor": {"primary_color": Colors.GREEN, "secondary_color": Colors.GOLD},
    "Boise State": {"primary_color": Colors.BLUE, "secondary_color": Colors.ORANGE},
    "UCLA": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
    "California": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
    "Cincinnati": {"primary_color": Colors.BLACK, "secondary_color": Colors.RED},
    "Clemson": {"primary_color": Colors.ORANGE, "secondary_color": Colors.WHITE},
    "Colorado": {"primary_color": Colors.GOLD, "secondary_color": Colors.BLACK},
    "Duke": {"primary_color": Colors.BLUE, "secondary_color": Colors.WHITE},
    "Florida": {"primary_color": Colors.BLUE, "secondary_color": Colors.ORANGE},
    "Florida State": {"primary_color": Colors.RED, "secondary_color": Colors.GOLD},
    "Georgia": {"primary_color": Colors.RED, "secondary_color": Colors.BLACK},
    "Georgia Tech": {"primary_color": Colors.GOLD, "secondary_color": Colors.WHITE},
    "Illinois": {"primary_color": Colors.ORANGE, "secondary_color": Colors.BLUE},
    "Indiana": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Iowa": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Iowa State": {"primary_color": Colors.GOLD, "secondary_color": Colors.RED},
    "Kansas": {"primary_color": Colors.BLUE, "secondary_color": Colors.RED},
    "Kansas State": {"primary_color": Colors.PURPLE, "secondary_color": Colors.WHITE},
    "Kentucky": {"primary_color": Colors.BLUE, "secondary_color": Colors.WHITE},
    "Louisville": {"primary_color": Colors.RED, "secondary_color": Colors.BLACK},
    "LSU": {"primary_color": Colors.PURPLE, "secondary_color": Colors.GOLD},
    "Maryland": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Miami": {"primary_color": Colors.ORANGE, "secondary_color": Colors.GREEN},
    "Michigan": {"primary_color": Colors.BLUE, "secondary_color": Colors.YELLOW},
    "Michigan State": {"primary_color": Colors.GREEN, "secondary_color": Colors.WHITE},
    "Minnesota": {"primary_color": Colors.RED, "secondary_color": Colors.GOLD},
    "Mississippi State": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Missouri": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Nebraska": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "UNC": {"primary_color": Colors.LIGHT_BLUE, "secondary_color": Colors.WHITE},
    "NC State": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Northwestern": {"primary_color": Colors.PURPLE, "secondary_color": Colors.WHITE},
    "Notre Dame": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
    "Ohio State": {"primary_color": Colors.RED, "secondary_color": Colors.GRAY},
    "Oklahoma": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Oklahoma State": {"primary_color": Colors.ORANGE, "secondary_color": Colors.BLACK},
    "Oregon": {"primary_color": Colors.GREEN, "secondary_color": Colors.YELLOW},
    "Oregon State": {"primary_color": Colors.ORANGE, "secondary_color": Colors.BLACK},
    "Penn State": {"primary_color": Colors.BLUE, "secondary_color": Colors.WHITE},
    "Pittsburgh": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
    "Purdue": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Rutgers": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "South Carolina": {"primary_color": Colors.BLACK, "secondary_color": Colors.RED},
    "Stanford": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Syracuse": {"primary_color": Colors.ORANGE, "secondary_color": Colors.BLUE},
    "TCU": {"primary_color": Colors.PURPLE, "secondary_color": Colors.WHITE},
    "Tennessee": {"primary_color": Colors.ORANGE, "secondary_color": Colors.WHITE},
    "Texas": {"primary_color": Colors.ORANGE, "secondary_color": Colors.WHITE},
    "Texas A&M": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Texas Tech": {"primary_color": Colors.RED, "secondary_color": Colors.BLACK},
    "Utah": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Vanderbilt": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Virginia": {"primary_color": Colors.ORANGE, "secondary_color": Colors.BLUE},
    "Virginia Tech": {"primary_color": Colors.ORANGE, "secondary_color": Colors.RED},
    "Wake Forest": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Washington": {"primary_color": Colors.PURPLE, "secondary_color": Colors.GOLD},
    "Washington State": {"primary_color": Colors.RED, "secondary_color": Colors.GRAY},
    "West Virginia": {"primary_color": Colors.GOLD, "secondary_color": Colors.BLUE},
    "Wisconsin": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "Wyoming": {"primary_color": Colors.GOLD, "secondary_color": Colors.BROWN},
    "Air Force": {"primary_color": Colors.BLUE, "secondary_color": Colors.WHITE},
    "Akron": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
    "Alabama-Birmingham": {
        "primary_color": Colors.GREEN,
        "secondary_color": Colors.GOLD,
    },
    "Appalachian State": {
        "primary_color": Colors.BLACK,
        "secondary_color": Colors.GOLD,
    },
    "Arkansas State": {"primary_color": Colors.RED, "secondary_color": Colors.BLACK},
    "Army": {"primary_color": Colors.BLACK, "secondary_color": Colors.GOLD},
    "Ball State": {"primary_color": Colors.RED, "secondary_color": Colors.WHITE},
    "AMCC": {"primary_color": Colors.BLUE, "secondary_color": Colors.GOLD},
}

COLOR_DICT = {
    "midnightblue": Colors.NAVY,
    "darkcyan": Colors.TEAL,
    "darkolivegreen": Colors.GREEN,
    "deepskyblue": Colors.LIGHT_BLUE,
    "mediumturquoise": Colors.LIGHT_BLUE,
    "darkslateblue": Colors.PURPLE,
    "darkgoldenrod": Colors.GOLD,
    "darkslategray": Colors.GRAY,
    "olive": Colors.GREEN,
    "darkgray": Colors.GRAY,
    "saddlebrown": Colors.BROWN,
    "darkblue": Colors.NAVY,
    "sienna": Colors.BROWN,
    "darksalmon": Colors.ORANGE,
    "cornflowerblue": Colors.LIGHT_BLUE,
    "limegreen": Colors.GREEN,
    "tomato": Colors.RED,
    "firebrick": Colors.RED,
    "mediumblue": Colors.BLUE,
    "skyblue": Colors.LIGHT_BLUE,
    "lavender": Colors.PURPLE,
    "indigo": Colors.PURPLE,
    "palegoldenrod": Colors.GOLD,
    "tan": Colors.BROWN,
    "lightslategray": Colors.GRAY,
    "brown": Colors.BROWN,
    "linen": Colors.WHITE,
    "white": Colors.WHITE,
    "peru": Colors.BROWN,
    "darkkhaki": Colors.BROWN,
    "sandybrown": Colors.ORANGE,
    "gold": Colors.GOLD,
    "red": Colors.RED,
    "forestgreen": Colors.GREEN,
    "seagreen": Colors.GREEN,
    "black": Colors.BLACK,
    "whitesmoke": Colors.WHITE,
    "gray": Colors.GRAY,
    "orangered": Colors.ORANGE,
    "gainsboro": Colors.GRAY,
    "chocolate": Colors.BROWN,
    "dodgerblue": Colors.BLUE,
    "crimson": Colors.RED,
    "goldenrod": Colors.GOLD,
    "cadetblue": Colors.BLUE,
    "maroon": Colors.RED,
    "teal": Colors.TEAL,
    "dimgray": Colors.GRAY,
    "darkgreen": Colors.GREEN,
    "purple": Colors.PURPLE,
    "orange": Colors.ORANGE,
    "silver": Colors.GRAY,
    "navy": Colors.NAVY,
    "darkorange": Colors.ORANGE,
    "lightblue": Colors.LIGHT_BLUE,
    "khaki": Colors.BROWN,
    "wheat": Colors.BROWN,
    "darkred": Colors.RED,
    "rosybrown": Colors.BROWN,
    "coral": Colors.ORANGE,
    "burlywood": Colors.BROWN,
    "steelblue": Colors.BLUE,
    "lightgray": Colors.GRAY,
}
