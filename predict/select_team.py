"""
Module for making predictions
"""

import random

from weight.lptr import lptr
from weight.sigmodal import sigmodal

import os
import sys

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django  # noqa: E402

django.setup()

from marchmadness.models.ap_ranking import APRanking  # noqa: E402


def random_selection(team_a, team_b, **kwargs):
    """
    Randomly selects a team

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Team
    """
    return random.choice([team_a, team_b])


def weighted_random_selection_lptr(team_a, team_b, **kwargs):
    return random.choices(
        population=[team_a, team_b],
        k=1,
        weights=lptr(team_a, team_b, ap_rank_weight=kwargs.get("ap_rank_weight", 0.75)),
    )[0]


def weighted_random_selection_sigmodal(team_a, team_b, **kwargs):
    return random.choices(
        population=[team_a, team_b],
        k=1,
        weights=sigmodal(
            team_a,
            team_b,
            ap_rank_weight=kwargs.get("ap_rank_weight", 0.75),
            k=kwargs.get("k", 0.33),
        ),
    )[0]


def ranked_selection(team_a, team_b, **kwargs):
    """
    Selects the team with the highest rank in the tournament. If ranks are the same,
    use AP Ranking. If both teams are unranked by the AP, select randomly.

    Avoiding calling ap_selection to prevent a circular use case

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Teamm_
    """
    if team_a.ranking < team_b.ranking:
        return team_a
    elif team_b.ranking < team_a.ranking:
        return team_b
    else:
        ap_rank_a = APRanking.objects.filter(school_name=team_a.school_name)
        if ap_rank_a:
            ap_rank_a = ap_rank_a.first().ranking
        ap_rank_b = APRanking.objects.filter(school_name=team_b.school_name)
        if ap_rank_b:
            ap_rank_b = ap_rank_b.first().ranking
        if ap_rank_a and ap_rank_b:
            if ap_rank_a < ap_rank_b:
                return team_a
            else:
                return team_b
        else:
            return random_selection(team_a, team_b)


def ap_selection(team_a, team_b, **kwargs):
    """
    Selects the team with the highest AP rank in the tournament. If both teams are
    unranked by the AP, use the tournament ranking. If tournament ranks are the same,
    select randomly.

    Avoiding calling ranked_selection to prevent a circular use case

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused


    Returns
    -------
    Team
    """
    ap_rank_a = APRanking.objects.filter(school_name=team_a.school_name)
    if ap_rank_a:
        ap_rank_a = ap_rank_a.first().ranking
    ap_rank_b = APRanking.objects.filter(school_name=team_b.school_name)
    if ap_rank_b:
        ap_rank_b = ap_rank_b.first().ranking
    if ap_rank_a and ap_rank_b:
        if ap_rank_a < ap_rank_b:
            return team_a
        else:
            return team_b
    else:
        if team_a.ranking < team_b.ranking:
            return team_a
        elif team_b.ranking < team_a.ranking:
            return team_b
        else:
            return random_selection(team_a, team_b)
