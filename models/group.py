import os
import sys
from collections import OrderedDict

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()

from marchmadness.models.tournament_ranking import TournamentRanking


class Group:
    def __init__(
        self,
        year,
        region,
        prediction_method,
        prediction_method_kwargs,
    ):
        self.year = year
        self.region = region
        self.predict = prediction_method
        self.prediction_method_kwargs = prediction_method_kwargs
        self.teams = TournamentRanking.objects.filter(
            year=self.year, region=self.region
        )
        self.one = self.teams.filter(ranking=1).first()
        self.two = self.teams.filter(ranking=2).first()
        self.three = self.teams.filter(ranking=3).first()
        self.four = self.teams.filter(ranking=4).first()
        self.five = self.teams.filter(ranking=5).first()
        self.six = self.teams.filter(ranking=6).first()
        self.seven = self.teams.filter(ranking=7).first()
        self.eight = self.teams.filter(ranking=8).first()
        self.nine = self.teams.filter(ranking=9).first()
        self.ten = self.teams.filter(ranking=10).first()
        self.eleven = self.teams.filter(ranking=11).first()
        self.twelve = self.teams.filter(ranking=12).first()
        self.thirteen = self.teams.filter(ranking=13).first()
        self.fourteen = self.teams.filter(ranking=14).first()
        self.fifteen = self.teams.filter(ranking=15).first()
        self.sixteen = self.teams.filter(ranking=16).first()

    @property
    def ranking_dict(self):
        rankings = {
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine,
            10: self.ten,
            11: self.eleven,
            12: self.twelve,
            13: self.thirteen,
            14: self.fourteen,
            15: self.fifteen,
            16: self.sixteen,
        }
        play_in_teams = self.teams.filter(play_in=True)
        play_in_rank = play_in_teams.first().ranking
        rankings[play_in_rank] = play_in_teams[0], play_in_teams[1]
        return rankings

    def first_four(self):
        play_in_teams = self.teams.filter(play_in=True)
        first_four_winner = self.predict(
            play_in_teams[0],
            play_in_teams[1],
            region=self.region,
            round_name="First Four",
            **self.prediction_method_kwargs,
        )
        if first_four_winner.ranking == 16:
            self.sixteen = first_four_winner
        elif first_four_winner.ranking == 15:
            self.fifteen = first_four_winner
        elif first_four_winner.ranking == 14:
            self.fourteen = first_four_winner
        elif first_four_winner.ranking == 13:
            self.thirteen = first_four_winner
        elif first_four_winner.ranking == 12:
            self.twelve = first_four_winner
        elif first_four_winner.ranking == 11:
            self.eleven = first_four_winner
        elif first_four_winner.ranking == 10:
            self.ten = first_four_winner
        else:
            raise ValueError("Unhandled play-in rank")
        return first_four_winner

    def first_round(self):
        return OrderedDict(
            {
                "1_16": self.predict(
                    self.one,
                    self.sixteen,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "8_9": self.predict(
                    self.eight,
                    self.nine,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "5_12": self.predict(
                    self.five,
                    self.twelve,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "4_13": self.predict(
                    self.four,
                    self.thirteen,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "6_11": self.predict(
                    self.six,
                    self.eleven,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "3_14": self.predict(
                    self.three,
                    self.fourteen,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "7_10": self.predict(
                    self.seven,
                    self.ten,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "2_15": self.predict(
                    self.two,
                    self.fifteen,
                    region=self.region,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def second_round(self, first_round_results):
        return OrderedDict(
            {
                "1_8": self.predict(
                    first_round_results["1_16"],
                    first_round_results["8_9"],
                    region=self.region,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "4_5": self.predict(
                    first_round_results["4_13"],
                    first_round_results["5_12"],
                    region=self.region,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "3_6": self.predict(
                    first_round_results["3_14"],
                    first_round_results["6_11"],
                    region=self.region,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "2_7": self.predict(
                    first_round_results["2_15"],
                    first_round_results["7_10"],
                    region=self.region,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def sweet_sixteen(self, second_round_results):
        return OrderedDict(
            {
                "1_4": self.predict(
                    second_round_results["1_8"],
                    second_round_results["4_5"],
                    region=self.region,
                    round_name="Sweet Sixteen",
                    **self.prediction_method_kwargs,
                ),
                "2_3": self.predict(
                    second_round_results["2_7"],
                    second_round_results["3_6"],
                    region=self.region,
                    round_name="Sweet Sixteen",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def elite_eight(self, sweet_sixteen_results):
        return self.predict(
            sweet_sixteen_results["1_4"],
            sweet_sixteen_results["2_3"],
            region=self.region,
            round_name="Elite Eight",
            **self.prediction_method_kwargs,
        )
