class Group:
    def __init__(self, ranking_dict, prediction_method, play_in_rank):
        self.one = ranking_dict[1]
        self.two = ranking_dict[2]
        self.three = ranking_dict[3]
        self.four = ranking_dict[4]
        self.five = ranking_dict[5]
        self.six = ranking_dict[6]
        self.seven = ranking_dict[7]
        self.eight = ranking_dict[8]
        self.nine = ranking_dict[9]
        self.ten = ranking_dict[10]
        self.eleven = ranking_dict[11]
        self.twelve = ranking_dict[12]
        self.thirteen = ranking_dict[13]
        self.fourteen = ranking_dict[14]
        self.fifteen = ranking_dict[15]
        self.sixteen = ranking_dict[16]
        self.play_in = ranking_dict["play_in"]
        self.predict = prediction_method
        self.play_in_rank = play_in_rank
        self.play_in.tournament_rank = self.play_in_rank
        self.first_four_results = None
        self.first_round_results = None
        self.second_round_results = None
        self.sweet_sixteen_results = None
        self.group_winner = None

    @property
    def ranking_dict(self):
        return {
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
            "Play In": self.play_in,
        }

    def first_four(self):
        self.ranking_dict[self.play_in_rank] = self.predict(
            self.play_in, self.ranking_dict[self.play_in_rank]
        )
        return self.ranking_dict[self.play_in_rank]

    def first_round(self):
        return {
            "1_16": self.predict(self.one, self.sixteen),
            "2_15": self.predict(self.two, self.fifteen),
            "3_14": self.predict(self.three, self.fourteen),
            "4_13": self.predict(self.four, self.thirteen),
            "5_12": self.predict(self.five, self.twelve),
            "6_11": self.predict(self.six, self.eleven),
            "7_10": self.predict(self.seven, self.ten),
            "8_9": self.predict(self.eight, self.nine),
        }

    def second_round(self, first_round_results):
        return {
            "1_8": self.predict(
                first_round_results["1_16"], first_round_results["8_9"]
            ),
            "2_7": self.predict(
                first_round_results["2_15"], first_round_results["7_10"]
            ),
            "3_6": self.predict(
                first_round_results["3_14"], first_round_results["6_11"]
            ),
            "4_5": self.predict(
                first_round_results["4_13"], first_round_results["5_12"]
            ),
        }

    def sweet_sixteen(self, second_round_results):
        return {
            "1_4": self.predict(
                second_round_results["1_8"], second_round_results["4_5"]
            ),
            "2_3": self.predict(
                second_round_results["2_7"], second_round_results["3_6"]
            ),
        }

    def elite_eight(self, sweet_sixteen_results):
        return self.predict(sweet_sixteen_results["1_4"], sweet_sixteen_results["2_3"])