"""
Module for adding relevant data to a DataFrame
"""

from data.colors import get_all_school_colors
from data.rivals import RIVALRIES
from data.names import FORMAL_TO_ABBREV, update_school_name
from helpers.soup_helpers import get_table
from fuzzywuzzy import fuzz
import pandas as pd
import regex

DI_SCHOOLS = "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_institutions"
D1_BASKETBALL_SCHOOLS = (
    "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_basketball_programs"
)
DASH_REGEX = regex.compile(r"\p{Pd}")
HAWAII_REGEX = regex.compile(r"ʻ")
MANOA_REGEX = regex.compile(r"ā")


def get_all_d1_schools():
    table = get_table(D1_BASKETBALL_SCHOOLS)
    columns = [c.string.strip() for c in table.find_all("th")]
    additional_rows = ["AP Ranking", "Tournament Ranking"]
    for r in additional_rows:
        columns.append(r)
    all_school_data = list()
    for school in table.find_all("tr")[1:]:
        school_data = list()
        for d in school.find_all("td"):
            content = d.string
            if not content:
                content = d.find("a").text
            content = content.strip()
            content = DASH_REGEX.sub("-", content)
            content = HAWAII_REGEX.sub("", content)
            content = MANOA_REGEX.sub("a", content)
            school_data.append(content)
        for _ in additional_rows:
            school_data.append(None)
        all_school_data.append(school_data)
    return pd.DataFrame(all_school_data, columns=columns)


def add_names_to_schools(df):
    for i, row in df.iterrows():
        school_name = row["School"]
        split_school_name = school_name.split(" ")
        spscnl = len(split_school_name)
        if school_name in FORMAL_TO_ABBREV:
            df.at[i, "Name"] = FORMAL_TO_ABBREV.get(school_name)
        elif (
            (spscnl == 3 or spscnl == 4)
            and school_name.startswith("University of")
            and "University of the Pacific" not in school_name
        ):
            df.at[i, "Name"] = " ".join(split_school_name[2:])
        elif school_name.endswith("University") or school_name.endswith("College"):
            df.at[i, "Name"] = " ".join(school_name.split(" ")[:-1])
        else:
            df.at[i, "Name"] = school_name


def add_team_colors_to_dataframe(session, df):
    data = get_all_school_colors(session)
    for i, row in df.iterrows():
        if row["Name"] in data:
            df.at[i, "Primary Color"] = data[row["Name"]]["primary_color"]
            df.at[i, "Secondary Color"] = data[row["Name"]]["secondary_color"]


def add_location_and_is_private_to_dataframe(df):
    schools_table = get_table(DI_SCHOOLS, 1)
    school_data = list()
    for row in schools_table.find_all("tr")[2:]:
        data = row.find_all("td")
        school = data[0].find("a").text
        location = f"{data[3].find('a').text}, {data[4].find('a').text}"
        is_private = data[5].find("a").text.casefold() == "private".casefold()
        school_data.append((school, location, is_private))
    for i, row in df.iterrows():
        best_index, best_ratio = school_index_in_tuple(row["School"], school_data)
        if best_ratio > 95:
            df.at[i, "Location"] = school_data[best_index][1]
            df.at[i, "Is Private"] = school_data[best_index][2]


def add_rivals_to_dataframe(df):
    df["Rivals"] = df["Name"].map(RIVALRIES)


def school_index_in_tuple(df_school, data):
    best_ratio = 0
    best_index = -1
    for j, (school, _, _) in enumerate(data):
        formal_name = update_school_name(school)
        for q, r in [("St.", "Saint"), ("The ", "")]:
            formal_name.replace(q, r)
            df_school.replace(q, r)
        split_formal_name = formal_name.casefold().split(" ")
        split_df_school = df_school.casefold().split(" ")
        generic = "University"
        if (
            split_formal_name[-1] == generic.casefold()
            and split_df_school[-1] == generic.casefold()
        ):
            ratio = fuzz.ratio(
                " ".join(split_df_school[:-1]), " ".join(split_formal_name[:-1])
            )
        elif (
            split_formal_name[0] == generic.casefold()
            and split_df_school[0] == generic.casefold()
        ):
            ratio = fuzz.ratio(
                " ".join(split_df_school[1:]), " ".join(split_formal_name[1:])
            )
        else:
            ratio = fuzz.ratio(df_school, formal_name)
        if ratio > best_ratio:
            best_ratio = ratio
            best_index = j
    return best_index, best_ratio


def filter_none_values(df, attribute):
    return df[df[attribute].notnull()]


def add_data_to_dataframe(df, data_tuple_list, attribute):
    """

    Parameters
    ----------
    df: DataFrame
    data_tuple_list: tuple
        Form is (school, value of attribute)
    attribute: str
        Attribute being updated

    Returns
    -------
    DataFrame
    """
    for data in data_tuple_list:
        best_ratio = 0
        for i, row in df.iterrows():
            ratio = fuzz.ratio(row["Name"], data[0])
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = i
        try:
            df.at[best_index, attribute] = int(data[1])
        except ValueError:
            df.at[best_index, attribute] = data[1]
    return df
