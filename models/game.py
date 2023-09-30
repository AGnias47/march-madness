import dateutil.parser
from dateutil.relativedelta import relativedelta


class Game:
    __slots__ = ("date", "opponent", "score", "home_game", "win")

    def __init__(self, game_date, opponent, score, home_game, win):
        self.date = dateutil.parser.parse(game_date).date()
        if self.date.month > 4:
            self.date -= relativedelta(years=1)
        self.opponent = opponent
        self.score = score
        self.home_game = home_game
        self.win = win

    def to_dict(self):
        return {
            "game_date": self.date.strftime("%b %d"),
            "opponent": self.opponent,
            "score": self.score,
            "home_game": self.home_game,
            "win": self.win,
        }
