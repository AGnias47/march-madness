from django.contrib import admin

from .models.ap_ranking import APRanking
from .models.game import Game
from .models.rivalry import Rivalry
from .models.school import School
from .models.tournament import Tournament
from .models.tournament_ranking import TournamentRanking

admin.site.register(APRanking)
admin.site.register(Game)
admin.site.register(Rivalry)
admin.site.register(School)
admin.site.register(Tournament)
admin.site.register(TournamentRanking)
